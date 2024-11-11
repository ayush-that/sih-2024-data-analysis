import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os


class SIHAnalyzer:
    def __init__(self, data_path):
        """Initialize analyzer with path to data file (CSV or JSON)"""
        self.data_path = Path(data_path)
        self.df = self.load_data()
        self.setup_style()
        self.results_dir = "results"
        os.makedirs(self.results_dir, exist_ok=True)

    def load_data(self):
        """Load data from CSV or JSON file"""
        if self.data_path.suffix == ".csv":
            return pd.read_csv(self.data_path)
        elif self.data_path.suffix == ".json":
            return pd.read_json(self.data_path)
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")

    def setup_style(self):
        plt.style.use("seaborn-v0_8-darkgrid")

        self.colors = [
            "#3498db",
            "#2ecc71",
            "#e74c3c",
            "#f1c40f",
            "#9b59b6",
            "#1abc9c",
            "#e67e22",
            "#34495e",
            "#7f8c8d",
            "#16a085",
        ]

        plt.rcParams["font.family"] = "sans-serif"
        plt.rcParams["font.sans-serif"] = ["Arial"]
        plt.rcParams["axes.labelsize"] = 12
        plt.rcParams["axes.titlesize"] = 14
        plt.rcParams["xtick.labelsize"] = 10
        plt.rcParams["ytick.labelsize"] = 10

    def basic_stats(self):
        """Generate basic statistics about the data"""
        stats = {
            "Total Entries": len(self.df),
            "Unique States": self.df["State"].nunique(),
            "Unique Cities": self.df["City"].nunique(),
            "Top 5 States": self.df["State"].value_counts().head(),
            "Top 5 Cities": self.df["City"].value_counts().head(),
        }
        return stats

    def plot_top_states(self, n=10, save=True):
        data = self.df["State"].value_counts().head(n).reset_index()
        data.columns = ["State", "Count"]

        plt.figure(figsize=(12, 6))

        ax = sns.barplot(data=data, x="State", y="Count", palette=self.colors[:n])

        plt.title(
            "Top States by Number of Selected Teams",
            pad=20,
            fontsize=16,
            fontweight="bold",
        )

        for i, v in enumerate(data["Count"]):
            ax.text(i, v + 1, str(v), ha="center", va="bottom")

        ax.grid(axis="y", linestyle="--", alpha=0.7)
        ax.set_axisbelow(True)

        plt.xticks(rotation=45, ha="right")

        for spine in ax.spines.values():
            spine.set_alpha(0.5)

        plt.tight_layout()

        if save:
            save_path = os.path.join(self.results_dir, "top_states.png")
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Plot saved as {save_path}")

        plt.show()

    def plot_city_distribution(self, top_n=20, save=True):
        """Plot distribution of teams across top N cities"""
        data = self.df["City"].value_counts().head(top_n).reset_index()
        data.columns = ["City", "Count"]

        plt.figure(figsize=(15, 7))

        ax = sns.barplot(
            data=data, x="City", y="Count", palette=sns.color_palette("viridis", top_n)
        )

        plt.title(
            "Distribution of Teams Across Top Cities",
            pad=20,
            fontsize=16,
            fontweight="bold",
        )

        for i, v in enumerate(data["Count"]):
            ax.text(i, v + 0.5, str(v), ha="center", va="bottom")

        ax.grid(axis="y", linestyle="--", alpha=0.7)
        ax.set_axisbelow(True)

        plt.xticks(rotation=45, ha="right")

        plt.tight_layout()

        if save:
            save_path = os.path.join(self.results_dir, "city_distribution.png")
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Plot saved as {save_path}")

        plt.show()

    def state_city_heatmap(self, top_states=10, top_cities=10, save=True):
        """Create a heatmap of top states vs top cities"""
        cross_tab = pd.crosstab(self.df["State"], self.df["City"])

        top_states = cross_tab.sum(axis=1).nlargest(top_states).index
        top_cities = cross_tab.sum(axis=0).nlargest(top_cities).index

        plt.figure(figsize=(12, 8))

        sns.heatmap(
            cross_tab.loc[top_states, top_cities],
            annot=True,
            fmt="d",
            cmap="viridis",
            cbar_kws={"label": "Number of Teams"},
            annot_kws={"size": 8},
            square=True,
        )

        plt.title("State vs City Distribution", pad=20, fontsize=16, fontweight="bold")

        plt.xlabel("City", labelpad=10)
        plt.ylabel("State", labelpad=10)

        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)

        plt.tight_layout()

        if save:
            save_path = os.path.join(self.results_dir, "state_city_heatmap.png")
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Plot saved as {save_path}")

        plt.show()

    def create_summary_dashboard(self, save=True):
        plt.style.use("dark_background")
        fig = plt.figure(figsize=(20, 12))

        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        ax1 = fig.add_subplot(gs[0, 0])
        state_data = self.df["State"].value_counts().head(8)
        sns.barplot(x=state_data.values, y=state_data.index, palette="viridis", ax=ax1)
        ax1.set_title("Top States", pad=20, fontsize=14, fontweight="bold")
        ax1.set_xlabel("Number of Teams")

        ax2 = fig.add_subplot(gs[0, 1])
        city_data = self.df["City"].value_counts().head(8)
        sns.barplot(x=city_data.values, y=city_data.index, palette="magma", ax=ax2)
        ax2.set_title("Top Cities", pad=20, fontsize=14, fontweight="bold")
        ax2.set_xlabel("Number of Teams")

        ax3 = fig.add_subplot(gs[1, :])
        cross_tab = pd.crosstab(self.df["State"], self.df["City"])
        top_states = cross_tab.sum(axis=1).nlargest(6).index
        top_cities = cross_tab.sum(axis=0).nlargest(8).index
        sns.heatmap(
            cross_tab.loc[top_states, top_cities],
            cmap="coolwarm",
            annot=True,
            fmt="d",
            cbar_kws={"label": "Number of Teams"},
            ax=ax3,
        )
        ax3.set_title(
            "State vs City Distribution", pad=20, fontsize=14, fontweight="bold"
        )

        fig.suptitle(
            "SIH Teams Analysis Dashboard", fontsize=16, fontweight="bold", y=0.95
        )

        plt.tight_layout()

        if save:
            save_path = os.path.join(self.results_dir, "sih_dashboard.png")
            plt.savefig(
                save_path,
                dpi=300,
                bbox_inches="tight",
                facecolor="black",
                edgecolor="none",
            )
            print(f"Dashboard saved as {save_path}")

        plt.show()


def main():
    analyzer = SIHAnalyzer("combined_sih_data.csv")

    print("\nBasic Statistics:")
    stats = analyzer.basic_stats()
    for key, value in stats.items():
        print(f"\n{key}:")
        print(value)

    print("\nGenerating visualizations...")
    analyzer.plot_top_states()
    analyzer.plot_city_distribution()
    analyzer.state_city_heatmap()
    analyzer.create_summary_dashboard()


if __name__ == "__main__":
    main()
