import logging
from datetime import datetime
import os

from geojson import load as load_geojson, dump as dump_geojson

from fastapi import FastAPI, APIRouter, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

from models.api.AvailableParametersResponse import AvailableParametersResponse
from models.api.CalculateTripRequestBody import CalculateTripRequestBody
from models.api.CalculateTripResponse import CalculateTripResponse

from algorithms.moves.AvailableMoves import AvailableMoves
from algorithms.AvailableAlgorithms import AvailableAlgorithms

from algorithms.Solver import Solver
from algorithms.TripProblem import TripProblem
from algorithms.AlgorithmStatistics import AlgorithmStatistics


environment = os.environ.get("ENV", "prod")
os.makedirs("./logs/api", exist_ok=True)
os.makedirs("./logs/paths", exist_ok=True)
os.makedirs("./logs/solutions", exist_ok=True)


logging.basicConfig(
    filename=f"./logs/backend-{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log",
    encoding="utf-8",
    format="%(levelname)s:%(message)s",
    level=logging.DEBUG if environment == "dev" else logging.INFO,
)
logger = logging.getLogger(__name__)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

dev_router = APIRouter()


@app.get("/available-parameters")
def available_parameters() -> AvailableParametersResponse:
    return AvailableParametersResponse(
        moves=[move.value for move in AvailableMoves],
        algorithms=[algorithm.value for algorithm in AvailableAlgorithms],
    )


@app.post("/calculate-trip")
def calculate_trip(
    trip_params: CalculateTripRequestBody,
    query_move: Annotated[AvailableMoves, Query(alias="move")],
    query_algorithm: Annotated[AvailableAlgorithms, Query(alias="algorithm")],
) -> CalculateTripResponse:
    current_time = datetime.now()
    if logger.isEnabledFor(logging.DEBUG):
        with open(
            f"./logs/api/{current_time.strftime('%Y-%m-%d_%H:%M:%S')}-calculate-trip-request.json",
            "w",
        ) as fp:
            request = trip_params.model_dump()
            request["query/move"] = query_move.value
            request["query/algorithm"] = query_algorithm.value
            dump_geojson(request, fp, indent=2)

    move_class = AvailableMoves.get_move(query_move)
    algorithm_class = AvailableAlgorithms.get_algorithm(query_algorithm)

    problem = TripProblem(trip_params, move_class)
    algorithm_statistics = AlgorithmStatistics(query_algorithm.value, query_move.value)
    algorithm = algorithm_class(problem, algorithm_statistics)
    solver = Solver(problem, algorithm)

    print(
        f"      INFO   [{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] Solving the problem using {query_algorithm.value} with {query_move.value}"
    )
    solution_state = solver.solve()
    print(
        f"      INFO   [{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] Solved the problem"
    )

    with open(
        f"./logs/solutions/{current_time.strftime('%Y-%m-%d_%H:%M:%S')}-statistics.json",
        "w",
    ) as fp:
        dump_geojson(algorithm_statistics.to_dict(), fp, indent=2)

    processed_solution = problem.process_solution(solution_state)
    trip_response = CalculateTripResponse(
        route=processed_solution["route"],
        geometry=processed_solution["geometry"],
    )

    if logger.isEnabledFor(logging.DEBUG):
        with open(
            f"./logs/api/{current_time.strftime('%Y-%m-%d_%H:%M:%S')}-calculate-trip-response.json",
            "w",
        ) as fp:
            response = trip_response.model_dump()
            response["query/move"] = query_move.value
            response["query/algorithm"] = query_algorithm.value
            dump_geojson(response, fp, indent=2)

    return trip_response


@dev_router.post("/calculate-trip-mock")
def calculate_trip_mock(
    trip_params: CalculateTripRequestBody,
    query_move: Annotated[AvailableMoves, Query(alias="move")],
    query_algorithm: Annotated[AvailableAlgorithms, Query(alias="algorithm")],
) -> CalculateTripResponse:
    with open("./mocks/calculate-trip-response-mock.json", "r") as fp:
        geojson = load_geojson(fp)
    return CalculateTripResponse(
        route=geojson["route"],
        geometry=geojson["geometry"],
    )


if environment == "dev":
    app.include_router(dev_router)
    print("      INFO   Development routes included")
    logger.info("Development routes included")
