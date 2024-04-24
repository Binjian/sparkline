import random
from statistics import mean
import pandas as pd
import matplotlib.pyplot as plt

from time import monotonic
from textual.app import App, ComposeResult
from textual.widgets import Sparkline, Header, Footer, Static
from textual.reactive import reactive

random.seed(73)
data = [random.expovariate(1 / 3) for _ in range(1000)]
# data = [random.expovariate(1 / 3) for _ in range(1000)]

df = pd.read_csv(r'./data/short_noise.csv')
df.set_index('second', inplace=True)
# data = df['speed'].tolist()

class SpeedControl(Static):
    """A static widget that displays the speed control in animation"""

    start_time = reactive(monotonic())
    time = reactive(0.0)


    def on_mount(self) -> None:
        self.set_interval(1, self.update_time)

    def update_time(self) -> None:
        self.time = monotonic() - self.start_time

    def watch_time(self, time: float) -> None:
        idx_so_far = int(time)
        speed_so_far = df['speed'].to_list()[:idx_so_far]
        lower_so_far = (df['lower']-df['speed']).to_list()[:idx_so_far]
        upper_so_far = (df['upper']-df['speed']).to_list()[:idx_so_far]
        self.query_one("#center").data = speed_so_far
        self.query_one("#lower").data = lower_so_far
        self.query_one("#upper").data = upper_so_far 

    def compose(self) -> ComposeResult:
        # yield Static("Speed Control")
        yield Sparkline(df['upper'].to_list(), summary_function=mean, id="upper")
        yield Sparkline(df['speed'].to_list(), summary_function=mean, id="center")
        yield Sparkline(df['lower'].to_list(), summary_function=mean, id="lower")



class SparklineSummaryFunctionApp(App[None]):
    CSS_PATH = "speed_control.tcss"

    def compose(self) -> ComposeResult:
        yield Static("Speed Control")
        yield SpeedControl()


app = SparklineSummaryFunctionApp()
if __name__ == "__main__":
    app.run()