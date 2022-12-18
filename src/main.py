from datetime import datetime
from concurrent import futures
import logging

import grpc

from grpc_generated_files import (
    RoutesAnalysis_pb2,
    RoutesAnalysis_pb2_grpc

)
from tmodel.time_model import Tmodel


class Routes(RoutesAnalysis_pb2_grpc.RoutesAnalysisServicer):
    def Analyse(self, request, context):
        date = request.timestamp
        date = datetime.fromtimestamp(date)
        model = Tmodel()
        params = [
                date.year,
                date.month,
                date.day,
                date.hour,
                request.distance,
                request.cargo_total,
                request.cargo_filled
            ]
        time_spent = model.predict(params)
        return RoutesAnalysis_pb2.AnalyseResponse(
            time_spent=time_spent[0]
        )


def serve():
    port = '7878'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    RoutesAnalysis_pb2_grpc.add_RoutesAnalysisServicer_to_server(
        Routes(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print(f"server listening on port {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
