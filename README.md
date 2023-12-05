
## 0. Construction de l'image
> ```docker build -t salogic .```


## 1. Exécution du script pour écouter les messages depuis rabbitMQ

> ```docker run  --network applications-networks salogic```

> ```docker exec -it --network applications-networks salogic sh 'python main.py' ```

1. Exécution du script pour envoyer les messages depuis rabbitMQ

> ```docker exec -it --network applications-networks salogic sh 'python send.py' ```
