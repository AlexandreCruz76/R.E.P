from flask import Flask, render_template, request
from solana.rpc.api import Client
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

app = Flask(__name__)

# Conectar ao cluster Solana
client = Client("https://api.mainnet-beta.solana.com")

# Configuração do banco de dados SQLite
engine = create_engine('sqlite:///wallets.db', echo=True)
Base = declarative_base()

class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True)
    assets = Column(Integer)
    tokens = Column(Integer)
    age = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        wallet_address = request.form['wallet_address']
        # Obter informações da carteira da Solana
        balance = client.get_balance(wallet_address)
        # Salvando no banco de dados
        new_wallet = Wallet(address=wallet_address, assets=balance['assets'], tokens=balance['tokens'])
        session.add(new_wallet)
        session.commit()
        return render_template('result.html', wallet_address=wallet_address, balance=balance)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
