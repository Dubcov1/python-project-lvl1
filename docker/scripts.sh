repo_name=$1
repo_login=$2
repo_password=$3

echo "$repo_password" | docker login --username "$repo_login" --password-stdin

(cd /docker/asterisk && docker build -t "$repo_name/test_asterisk" .)
docker push "$repo_name/test_asterisk"

docker pull mysql:5.7
docker tag mysql:5.7 "$repo_name/test_mysql"
docker push "$repo_name/test_mysql"

docker pull redis:latest
docker tag redis:latest "$repo_name/test_redis"
docker push "$repo_name/test_redis"

(cd /docker/applications && docker build -t "$repo_name/test_application" .)
docker push "$repo_name/test_application"

docker rmi "$repo_name/test_asterisk" "$repo_name/test_mysql" "$repo_name/test_redis" "$repo_name/test_application"

docker logout
