"""Entry point for __TITLE__."""

import hydra
from omegaconf import DictConfig


@hydra.main(version_base=None, config_path="../../conf", config_name="config")
def run(cfg: DictConfig) -> None:
    """Run the main pipeline.

    Args:
        cfg: Hydra configuration object.
    """
    print(f"Starting {cfg.project.name}")
    # TODO: implement pipeline stages


if __name__ == "__main__":
    run()
