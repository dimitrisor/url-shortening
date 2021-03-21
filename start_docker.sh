app_name="shorty"
app_version="latest"
docker build -t ${app_name}:${app_version} .
docker run -p 8080:5000 --name ${app_name} -d ${app_name}:${app_version}