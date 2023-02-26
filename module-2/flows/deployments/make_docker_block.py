from prefect.infrastructure.docker import DockerContainer

"""
This script creates dcker container blocks in prefect
"""
docker_block = DockerContainer(
    image="afrogrit/prefect:de",
    image_pull_policy="ALWAYS",
    auto_remove=True,
)

docker_block.save("zoom", overwrite=True)
