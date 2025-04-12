from prefect import flow, task

@task(log_prints=True)
def print_data():
    print("Primeira Execução da Task")

@flow(log_prints=True)
def init():
    print_data()

init()