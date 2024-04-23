import random
from statistics import mean

from textual.app import App, ComposeResult
from textual.widgets import Sparkline

random.seed(73)
data = [random.expovariate(1 / 3) for _ in range(1000)]


class SparklineSummaryFunctionApp(App[None]):
    CSS_PATH = "sparkline.tcss"

    def compose(self) -> ComposeResult:
        yield Sparkline(data, summary_function=max)  
        yield Sparkline(data, summary_function=mean)  
        yield Sparkline(data, summary_function=min)  


app = SparklineSummaryFunctionApp()
if __name__ == "__main__":
    app.run()