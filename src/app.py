from src.service import consumer

if __name__ == '__main__':
    print('STARTING APP', flush=True)
    consumer.consume()
