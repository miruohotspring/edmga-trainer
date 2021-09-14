from edmga_trainer.model import EDMGA_Trainer
from edmga_trainer import utils

def main():
    data_loader = utils.DataLoader()
    print(data_loader.genre_lists)

if __name__ == '__main__':
    main()
