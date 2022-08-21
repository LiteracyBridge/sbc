#!/usr/bin/env bash


function usage() {
    printf "USAGE: Specify a python filename in the current directory to deploy.\nThe lambda function name to be updated must match the python filename\n(without the '.py' extension).\n"
}

file=
if [ ! -z $1 ]; then
    file="$1"
    if [ ${file:0:1} == "-" ]; then
        usage
        exit 1
    fi
    printf "Installing dependencies, zipping, and deploying to AWS.\n\n"
else
    usage 
    exit 1
fi


file=$1
len=$((${#file}-3))
lambda_fct=${file:0:len}
rm -R package
pip install --target ./package pg8000
cd package
rm ../package.zip
zip -r ../package.zip .
cd ..
zip -g package.zip ${file}
aws lambda create-function --function-name ${lambda_fct}  --zip-file fileb://package.zip --handler ${lambda_fct}.lambda_handler --runtime python3.8 --role arn:aws:iam::856701711513:role/lambda-statistics-query
rm package.zip
