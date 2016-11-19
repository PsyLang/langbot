docker run -it --name=[your_container_name] -p [your_host_jupyter_port]:8888 -p [your_host_tensorboard_port]:6006 -e "TZ=Asia/Seoul" -v [your_host_directory]:/notebooks/work psylang/langbot:0.1
