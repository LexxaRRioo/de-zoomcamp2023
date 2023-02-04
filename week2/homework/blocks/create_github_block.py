from prefect.filesystems import GitHub

block = GitHub(
    repository="https://github.com/LexxaRRioo/de-zoomcamp2023",

)
block.get_directory("week2/homework") # specify a subfolder of repo
block.save("dev")