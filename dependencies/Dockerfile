
FROM public.ecr.aws/lambda/python:3.13


WORKDIR /var/task


RUN pip install --upgrade pip
RUN pip install pandas scikit-learn boto3 numpy


COPY detect_anomalies.py .  
COPY anomaly_model.pkl .  


CMD ["detect_anomalies.lambda_handler"]
