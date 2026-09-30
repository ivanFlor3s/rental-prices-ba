import argparse
import sys

from src.application.orchestors.scrap_map_save import ScrappingOrchestrator
from src.application.use_cases.export_csv import export_departments_to_csv
from src.application.use_cases.scrapper_health import ScrapperHealthCheckUseCase
from src.infrastructure.logging.config import logger


def run_scraping(neighborhoods: list[str] | None = None, operation: str = "rent"):
    orchestrator = ScrappingOrchestrator(operation=operation)

    if neighborhoods:
        result = orchestrator.scrap_specific_neighborhoods(neighborhoods)
    else:
        result = orchestrator.scrap_all_neighborhoods()

    logger.info(result.get_summary())
    return result


def run_health_check() -> None:
    report = ScrapperHealthCheckUseCase().check_zonaprop_health()
    logger.info(
        "Scrapper health check",
        source=report["source"],
        neighborhood_tested=report["neighborhood_tested"],
        status=report["status"],
        scraped_items=report["scraped_items"],
        fields_failing=report["fields_failing"],
        message=report["message"],
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rental-prices-ba",
        description="Scrapper y persistencia de precios de alquileres en Buenos Aires.",
    )
    parser.add_argument(
        "neighborhoods",
        nargs="*",
        help="Barrios específicos a scrapear. Si se omite, se scrapean todos.",
    )
    parser.add_argument(
        "--export-csv",
        metavar="FILE",
        nargs="?",
        const="departments.csv",
        default=None,
        help="Exporta los departamentos persistidos a CSV (por defecto departments.csv).",
    )
    parser.add_argument(
        "--health",
        action="store_true",
        help="Chequea la salud de los selectores DOM del scrapper de ZonaProp.",
    )
    parser.add_argument(
        "--operation",
        choices=["rent", "sale", "both"],
        default="rent",
        help="Tipo de operación a scrapear: rent (alquiler), sale (venta) o both. Default: rent.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.health:
        run_health_check()
        return

    if args.export_csv:
        export_departments_to_csv(args.export_csv)
        return

    neighborhoods = args.neighborhoods or None
    if args.operation == "both":
        for operation in ("rent", "sale"):
            logger.info(f"Scraping operation: {operation}")
            run_scraping(neighborhoods, operation)
    else:
        run_scraping(neighborhoods, args.operation)


if __name__ == "__main__":
    main()
