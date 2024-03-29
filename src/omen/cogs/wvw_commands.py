# src/cogs/wvw_commands.py
import os
import discord
import logging
from discord.ext import tasks, commands
from discord import app_commands
from functions import to_lower, attach_image, return_script_dir
import pandas
from pandas import DataFrame
from pandas import RangeIndex
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from skforecast.ForecasterAutoregMultiSeries import ForecasterAutoregMultiSeries
from skforecast.model_selection_multiseries import backtesting_forecaster_multiseries
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
from datetime import datetime
import pytz

from api.gw2_api import GW2Wrapper

class WVWCommands(commands.GroupCog, name="wvw"):
    def __init__(self, omen_bot):
        super().__init__()
        self.omen_bot = omen_bot
        self.logger = logging.getLogger("omen_bot_logger")
        self.gw2_api = GW2Wrapper()
        self.img_world_population = "world_population.png"
        self.server_colors = [ 'green', 'blue', 'red' ]
        self.wvw_batch_update.add_exception_type(discord.app_commands.errors.CommandInvokeError)
        self.wvw_batch_update.start()

        # Internal dictionary to house match data - not required, but helpful to visualize
        self.match_data_dict = {
            'last_update': '',
            'tier': '',
            'prediction_quality': -1, # Lower is better, -1 means no prediction
            'blue': {
                'worlds': {
                    'host': '',
                    'link': ''
                },
                'victory_points': 0,
                'predicted_victory_points': 0,
                'kd': {
                    'kills': 0,
                    'deaths': 0,
                    'kdr': 0
                },
                'objectives': {
                    'camp': 0,
                    'tower': 0,
                    'keep': 0,
                    'castle': 0
                },
                "skirmish": {
                    'skirmish_scores': {},
                    'ppt': 0
                }
            },
            'green': {
                'worlds': {
                    'host': '',
                    'link': ''
                },
                'victory_points': 0,
                'predicted_victory_points': 0,
                'kd': {
                    'kills': 0,
                    'deaths': 0,
                    'kdr': 0
                },
                'objectives': {
                    'camp': 0,
                    'tower': 0,
                    'keep': 0,
                    'castle': 0
                },
                "skirmish": {
                    'skirmish_scores': {},
                    'ppt': 0
                }
            },
            'red': {
                'worlds': {
                    'host': '',
                    'link': ''
                },
                'victory_points': 0,
                'predicted_victory_points': 0,
                'kd': {
                    'kills': 0,
                    'deaths': 0,
                    'kdr': 0
                },
                'objectives': {
                    'camp': 0,
                    'tower': 0,
                    'keep': 0,
                    'castle': 0
                },
                "skirmish": {
                    'skirmish_scores': {},
                    'ppt': 0
                }
            }
        }

    # Populate class dictionary with VP data
    async def get_current_victory_points(self, match_data):     
        try:
            for server, points in match_data['victory_points'].items():
                self.match_data_dict[server]['victory_points'] = points
        except Exception as e:
                self.match_data_dict[server]['victory_points'] = self.match_data_dict[server]['victory_points']

    # Populate class dictionary with K/D data
    async def get_current_kdr(self, match_data):
        # Collect kills
        try:
            for server, k_or_d in match_data['kills'].items():
                self.match_data_dict[server]['kd']['kills'] = k_or_d
        except Exception as e:
            self.logger.error(f"Error in get_current_kdr: {e}")

        # Collect deaths
        for server, k_or_d in match_data['deaths'].items():
            self.match_data_dict[server]['kd']['deaths'] = k_or_d

        # Calc and store KDR
        for server, data in self.match_data_dict.items():
            try:
                if server in [ 'blue', 'green', 'red' ]:
                    self.match_data_dict[server]['kd']['kdr'] = round(data['kd']['kills'] / data['kd']['deaths'], 2) 
            except Exception as e:
                self.match_data_dict[server]['kd']['kdr'] = self.match_data_dict[server]['kd']['kdr']
                self.logger.error(f"Unable to calculate KDR in get_current_kdr: {e}")

    # Populate class dictionary with server data
    async def get_current_match_servers(self, match_data):
        try:
            for server, ids in match_data['all_worlds'].items():
                self.match_data_dict[server]['worlds']['host'] = self.gw2_api.worlds([ids[1]])[0]['name']
                self.match_data_dict[server]['worlds']['link'] = self.gw2_api.worlds([ids[0]])[0]['name']
        except Exception as e:
            self.logger.error(f"Problem in get_current_match_servers: {e}")

    # Populate class dictionary with owned objectives data
    async def get_owned_objectives(self, match_data):
        try:
            # We need to reset values in the self dict before proceeding since we are counting
            for s in self.server_colors:
                self.match_data_dict[s]['objectives'] = self.match_data_dict[s]['objectives'].fromkeys(self.match_data_dict[s]['objectives'], 0)
                self.match_data_dict[s]['skirmish']['ppt'] = 0
        except Exception as e:
            self.logger.error(f"Error in get_owned_objectives: {e}")

        objectives_to_count = [ 'camp', 'tower', 'keep', 'castle' ]
        map_count = len(match_data['maps'])
        map_iter = 0

        while map_iter < map_count:
            obj_count = len(match_data['maps'][map_iter]['objectives'])
            obj_iter = 0

            while obj_iter < obj_count:
                obj_owner = match_data['maps'][map_iter]['objectives'][obj_iter]['owner'].lower()
                obj_type = match_data['maps'][map_iter]['objectives'][obj_iter]['type'].lower()
                self.match_data_dict[obj_owner]['skirmish']['ppt'] += match_data['maps'][map_iter]['objectives'][obj_iter]['points_tick']
                try:
                    if obj_type in objectives_to_count: self.match_data_dict[obj_owner]['objectives'][obj_type] += 1
                except Exception as e:
                    print(e)
                obj_iter += 1
            map_iter += 1

    # Return tier for current matchup
    async def get_current_tier(self, match_data):
        try:
            self.match_data_dict['tier'] = match_data['id'].split('-')[1]
        except Exception as e:
            self.logger.error(f"Error in get_current_tier: {e}")
    
    # Populate dictionary with skirmish data
    async def get_skirmish_data(self, match_data):
        try:
            for skirmish in match_data['skirmishes']:
                for s in self.server_colors:
                    self.match_data_dict[s]['skirmish']['skirmish_scores'][skirmish['id']] = skirmish['scores'][s]
        except Exception as e:
            self.logger.error(f"Error in get_skirmish_data: {e}")
            return None

    async def predict_future_skirmish_data(self):
        try:
            # reset values in the self dict
            for s in self.server_colors:
                self.match_data_dict[s]['predicted_victory_points'] = 0

            # gather the relevant data
            data = {
                'skirmish_id': list(self.match_data_dict['green']['skirmish']['skirmish_scores'].keys())[:-1],
                'green_score': list(self.match_data_dict['green']['skirmish']['skirmish_scores'].values())[:-1],
                'blue_score': list(self.match_data_dict['blue']['skirmish']['skirmish_scores'].values())[:-1],
                'red_score': list(self.match_data_dict['red']['skirmish']['skirmish_scores'].values())[:-1]
            }
            completed_skirmishes = data['skirmish_id'][-1]
            total_skirmishes = 84

            if completed_skirmishes < 2:
                self.logger.info("Insufficient data to predict future skirmish data")
                return

            # format into dataframe
            past_skirmishes = DataFrame(data,
                index=RangeIndex(start=data['skirmish_id'][0], stop=completed_skirmishes + 1, name="skirmish"),
                columns=['green_score', 'blue_score', 'red_score'])

            # predict all the remaining skirmishes
            # TODO Additional testing and tuning on these four regressors.
            segments = min(len(past_skirmishes.index) - 1, 4)
            forecaster = ForecasterAutoregMultiSeries (
                #regressor = DecisionTreeRegressor(),
                regressor = KNeighborsRegressor(n_neighbors=min(completed_skirmishes, 5)),
                #regressor = RandomForestRegressor(),
                #regressor = GradientBoostingRegressor(),
                transformer_series = StandardScaler(),
                lags = segments
            )
            forecaster.fit(past_skirmishes)
            future_skirmishes = DataFrame(0,
                index=RangeIndex(start=completed_skirmishes+1, stop=total_skirmishes+1, name="skirmish"),
                columns=['green_score', 'blue_score', 'red_score'],
                )
            metric, predictions = backtesting_forecaster_multiseries(
                forecaster = forecaster,
                series = pandas.concat([past_skirmishes, future_skirmishes]),
                steps = total_skirmishes - segments,
                metric = 'mean_absolute_error',
                initial_train_size = None
            )

            # combine the predictions with the historical data to get a complete match
            match = pandas.concat([past_skirmishes, predictions.loc[completed_skirmishes+1:]])

            # crack open the metric value and compute the overall metrics.
            #self.logger.debug(f"\n{match.to_string()}\n{metric.to_string()}")

            # forecast end match victory points
            for skirmish in match.index:
                scores = match.loc[skirmish, ['green_score', 'blue_score', 'red_score']]
                ranks = scores.rank(ascending=False, method='min')
                for rank, team in zip(ranks, self.server_colors):
                    self.match_data_dict[team]['predicted_victory_points'] += (5 - (rank - 1))
            self.match_data_dict['prediction_quality'] = metric['mean_absolute_error'].mean()
        except Exception as e:
            self.logger.error(f"Error in predict_future_skirmish_data: {e}")
        
    # Generic function to get full WvW data for current match
    async def get_current_match_data(self):
        try:
            return self.gw2_api.wvw_matches(await self.get_current_world())
        except Exception as e:
            self.logger.error(f"Unable to retrieve data in get_current_match_data: {e}")
            return None

    # Return current world for Rall
    async def get_current_world(self):
        try:
            return self.gw2_api.account()['world']
        except Exception as e:
            self.logger.error(f"Unable to retrieve data in get_current_world: {e}")
            return '1014'

    # Get assets dir
    async def get_assets_dir(self):
        return os.path.join(return_script_dir(), 'assets')

    # Generate pie chart
    async def generate_score_piechart(self):
        try:
            file_path = os.path.join(await self.get_assets_dir(), "current_score.png")

            # Clear the figure to free up resources
            plt.clf()

            server_scores = [int(self.match_data_dict['green']['skirmish']['ppt']), int(self.match_data_dict['blue']['skirmish']['ppt']), int(self.match_data_dict['red']['skirmish']['ppt'])]
            plt.figure(figsize=(12, 12))

            patches, server_labels = plt.pie(
                server_scores,  
                rotatelabels=False, 
                labeldistance=0.70, 
                colors=['green', 'blue', 'red'],
                wedgeprops={'linewidth': 15.0, 'edgecolor': 'white'},
                )

            plt.savefig(file_path, transparent=True)
            plt.close()
        except Exception as e:
            self.logger.error(f"Error in generate_score_piechart: {e}")

    # Collect data on a schedule to lighten load 
    @tasks.loop(minutes=5.0, reconnect = True)
    async def wvw_batch_update(self):
        try:
            match_data = await self.get_current_match_data()

            await self.get_current_match_servers(match_data)
            await self.get_current_tier(match_data)
                    
            # Current victory points for each server
            await self.get_current_victory_points(match_data)

            # Current k/d for each server
            await self.get_current_kdr(match_data)

            # Current objectives for each server
            await self.get_owned_objectives(match_data)

            # Historical and current skirmish data
            await self.get_skirmish_data(match_data)

            # Make predictions based on skirmish data
            await self.predict_future_skirmish_data()

            # Update timestamp for last update
            new_york_timezone = pytz.timezone("America/New_York")
            now = datetime.now(new_york_timezone)
            self.match_data_dict['last_update'] = now.strftime("%d/%m/%Y %H:%M:%S")

            await self.generate_score_piechart()
        except Exception as e:
            self.logger.error(f"wvw_batch_update loop encountered an error: {e}")
            self.wvw_batch_update.restart()


    @wvw_batch_update.before_loop
    async def before_wvw_batch_update(self):
        await self.omen_bot.wait_until_ready()

    async def cog_unload(self):
        self.wvw_batch_update.cancel()

    @app_commands.command(name="matchup", description="Display information about our current WvW matchup")
    async def matchup(self, interaction: discord.Interaction):
        await interaction.response.defer()
        # General variables
        camp_emoji = "<:wvw_camp:1058165536334303272>"
        tower_emoji = "<:wvw_towe:1058167072762384414>"
        keep_emoji = "<:wvw_keep:1058165533532500108>"
        castle_emoji = "<:wvw_cast:1058165532366487572>"
        icon_image = "icon_author_co.jpg" 
        thumb_image = "current_score.png"
        embed_obj_value_string = ""
        embed_skirmish_value_string = ""
        embed_predicted_victory_points_string = ""
        
        author_img_attached = attach_image("icon_author_co.jpg")
        thumb_img_attached = attach_image("current_score.png")
        
        try:
            embed=discord.Embed(title="Current Matchup", url="https://wvwintel.com/#1014", description=f"__Tier {self.match_data_dict['tier']}__", color=0xa8009a)
            embed.set_author(name="Omen", url="https://github.com/Phloot/omen-bot/", icon_url=f"attachment://{icon_image}")
            embed.set_thumbnail(url=f"attachment://{thumb_image}")

            for server in self.server_colors:
                embed.add_field(
                    name=f":{server}_circle: {server.title()}", 
                    value=f"{self.match_data_dict[server]['worlds']['host']}\n{self.match_data_dict[server]['worlds']['link']}\n\n"
                    f"**Victory Points**: {self.match_data_dict[server]['victory_points']}\n**K/D**: {self.match_data_dict[server]['kd']['kdr']}", 
                    inline=True
                )
                embed_obj_value_string += f":{server}_circle: {camp_emoji}x{self.match_data_dict[server]['objectives']['camp']} {tower_emoji}x{self.match_data_dict[server]['objectives']['tower']} {keep_emoji}x{self.match_data_dict[server]['objectives']['keep']} {castle_emoji}x{self.match_data_dict[server]['objectives']['castle']}\n"
                embed_skirmish_value_string += f":{server}_circle: Points: {self.match_data_dict[server]['skirmish']['skirmish_scores'][list(self.match_data_dict[server]['skirmish']['skirmish_scores'])[-1]]} (+{self.match_data_dict[server]['skirmish']['ppt']} per tick)\n"
                embed_predicted_victory_points_string += f":{server}_circle: Predicted Points: {int(self.match_data_dict[server]['predicted_victory_points'])}\n"
            #TODO Cleanly output when there's no prediction
            #embed_predicted_victory_points_string += f"Prediction Quality (lower is better): {str(round(self.match_data_dict['prediction_quality'], 2))}"
            embed.add_field(name=f"Current Skirmish ({list(self.match_data_dict[server]['skirmish']['skirmish_scores'])[-1]} of 84)", value=embed_skirmish_value_string, inline=True)
            embed.add_field(name="Match Prediction", value=embed_predicted_victory_points_string, inline=True)
            embed.add_field(name="Objectives", value=embed_obj_value_string, inline=False)
            embed.set_footer(text=f"Data last updated at {self.match_data_dict['last_update']}")
            await interaction.followup.send(files=[author_img_attached, thumb_img_attached], embed=embed)
        except Exception as e:
            print(e)

    @app_commands.command(name="worldpop", description="Display current population tiers for a region")
    @app_commands.describe(option="Select a region to check populations for")
    @app_commands.choices(option=[
        app_commands.Choice(name="North America", value="na"),
        app_commands.Choice(name="Europe", value="eu")
    ])
    async def worldpop(self, interaction: discord.Interaction, option: app_commands.Choice[str]):
        await interaction.response.defer()
        if option.value not in [ 'na', 'eu' ]:
            raise commands.BadArgument(f"Invalid argument {option.value} provided!")

        img_flag = f"flag_{option.value}.png"
        icon_image = "icon_author_co.jpg" 
        
        world_list_all = self.gw2_api.worlds()

        if option.value == "na":
            bar_color = 0x0c09ec
            world_list_region = [world for world in world_list_all if world['id'] < 2000]
        elif option.value == "eu":
            bar_color = 0xffd700
            world_list_region = [world for world in world_list_all if world['id'] > 2000]
        
        # Attach images to display
        author_img_attached = attach_image("icon_author_co.jpg")
        thumbnail_img_attached = attach_image(img_flag)

        # Initialize the embed
        embed=discord.Embed(title=f"Current {option.value.upper()} World Populations", color=bar_color)
        embed.set_author(name="Omen", url="https://github.com/Phloot/omen-bot/", icon_url=f"attachment://{icon_image}")
        embed.set_thumbnail(url=f"attachment://{img_flag}")
        embed.add_field(name=":red_circle: Full", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "Full"]))
        embed.add_field(name=":orange_circle: Very High", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "VeryHigh"]))
        embed.add_field(name=":yellow_circle: High", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "High"]))
        embed.add_field(name=":green_circle: Medium", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "Medium"]))
        #embed.add_field(name=":green_circle: Low", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "Low"]))
        await interaction.followup.send(files=[author_img_attached, thumbnail_img_attached], embed=embed)

async def setup(omen_bot):
    await omen_bot.add_cog(WVWCommands(omen_bot))
