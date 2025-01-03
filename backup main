from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
import jwt
import bcrypt
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

# Configurações
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "sua_chave_secreta_aqui")  # Não use esta chave em produção
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuração do FastAPI
app = FastAPI(title="API de Laudos Psicológicos")

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Model SQLAlchemy
class UserModel(Base):
    __tablename__ = "usuarios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    crp = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# Criar tabelas
Base.metadata.create_all(bind=engine)


# Models Pydantic
class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    crp: str


class User(BaseModel):
    id: str
    nome: str
    email: EmailStr
    crp: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    email: str
    senha: str


# Funções auxiliares
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Rotas
@app.post("/users/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar se usuário já existe
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")

    # Hash da senha
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.senha.encode('utf-8'), salt)

    # Criar novo usuário
    db_user = User(
        nome=user.nome,
        email=user.email,
        senha_hash=hashed_password.decode('utf-8'),
        crp=user.crp
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not bcrypt.checkpw(form_data.password.encode('utf-8'), user.senha_hash.encode('utf-8')):
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


# Rotas
@app.post("/auth/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:s
        raise HTTPException(status_code=400, detail="Email já registrado")

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.senha.encode('utf-8'), salt)

    db_user = UserModel(
        nome=user.nome,
        email=user.email,
        senha_hash=hashed_password.decode('utf-8'),
        crp=user.crp
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/auth/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == login_data.email).first()
    if not user or not bcrypt.checkpw(login_data.senha.encode('utf-8'), user.senha_hash.encode('utf-8')):
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos"
        )

    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/auth/me", response_model=User)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


# Novas rotas para gerenciar histórico
@app.get("/laudos", response_model=List[LaudoResponse])
async def listar_laudos(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    laudos = db.query(Laudo).filter(
        Laudo.usuario_id == current_user.id
    ).order_by(Laudo.criado_em.desc()).all()
    return laudos


@app.get("/laudos/{laudo_id}")
async def obter_laudo(
        laudo_id: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    laudo = db.query(Laudo).filter(
        Laudo.id == laudo_id,
        Laudo.usuario_id == current_user.id
    ).first()

    if not laudo:
        raise HTTPException(status_code=404, detail="Laudo não encontrado")

    return laudo


@app.get("/laudos/{laudo_id}/pdf")
async def gerar_pdf_laudo(
        laudo_id: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    laudo = db.query(Laudo).filter(
        Laudo.id == laudo_id,
        Laudo.usuario_id == current_user.id
    ).first()

    if not laudo:
        raise HTTPException(status_code=404, detail="Laudo não encontrado")

    # Criar PDF
    pdf_path = f"temp/laudo_{laudo_id}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Adicionar conteúdo ao PDF
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Laudo Psicológico")

    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Paciente: {laudo.paciente.nome}")
    c.drawString(50, 700, f"Data: {laudo.criado_em.strftime('%d/%m/%Y')}")
    c.drawString(50, 680, f"Psicólogo: {current_user.nome} - CRP: {current_user.crp}")

    # Adicionar diagnóstico
    text_object = c.beginText(50, 650)
    text_object.setFont("Helvetica", 12)

    # Quebrar o texto em linhas
    wrapped_text = textwrap.fill(laudo.diagnostico, width=80)
    for line in wrapped_text.split('\n'):
        text_object.textLine(line)

    c.drawText(text_object)
    c.save()

    # Retornar o arquivo PDF
    return FileResponse(
        pdf_path,
        filename=f"laudo_{laudo_id}.pdf",
        media_type="application/pdf"
    )


# Rota para atualizar um laudo
@app.put("/laudos/{laudo_id}")
async def atualizar_laudo(
        laudo_id: str,
        diagnostico: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    laudo = db.query(Laudo).filter(
        Laudo.id == laudo_id,
        Laudo.usuario_id == current_user.id
    ).first()

    if not laudo:
        raise HTTPException(status_code=404, detail="Laudo não encontrado")

    laudo.diagnostico = diagnostico
    laudo.atualizado_em = datetime.utcnow()

    db.commit()
    return laudo

@app.post("/diagnostico/ia")
async def analisar_diagnostico_ia(
    texto: str,
    current_user: User = Depends(get_current_user)
):
    resultado = await processar_diagnostico_ia(texto)
    return resultado


class AssistenteIA:
    def __init__(self):
        # Carregar modelo de linguagem pré-treinado
        self.tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
        self.modelo = AutoModelForSequenceClassification.from_pretrained(
            "neuralmind/bert-base-portuguese-cased",
            num_labels=10  # Categorias de transtornos mentais
        )

        # Carregar modelo de processamento de linguagem natural
        self.nlp = spacy.load("pt_core_news_sm")

        # Base de conhecimento de sintomas e possíveis diagnósticos
        self.base_sintomas = pd.read_csv('base_sintomas.csv')

    def extrair_entidades_chave(self, texto):
        """
        Extrai entidades chave do texto usando processamento de linguagem natural
        """
        doc = self.nlp(texto)
        entidades = {
            'sintomas': [],
            'comportamentos': [],
            'emoções': []
        }

        for ent in doc.ents:
            if ent.label_ in ['PER', 'MISC']:
                entidades['sintomas'].append(ent.text)

        return entidades

    def analisar_texto_diagnostico(self, texto):
        """
        Realizar classificação preliminar usando modelo de linguagem
        """
        inputs = self.tokenizer(
            texto,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        outputs = self.modelo(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)

        # Mapear probabilidades para categorias de transtornos
        categorias = [
            'Depressão',
            'Ansiedade',
            'Transtorno Bipolar',
            'Estresse Pós-Traumático',
            'Transtorno de Pânico',
            'Transtorno Obsessivo-Compulsivo',
            'Transtorno de Personalidade',
            'Transtorno de Alimentação',
            'Transtorno de Déficit de Atenção',
            'Sem Indicação Específica'
        ]

        resultados = [
            {'categoria': cat, 'probabilidade': prob.item()}
            for cat, prob in zip(categorias, probabilities[0])
        ]

        return sorted(resultados, key=lambda x: x['probabilidade'], reverse=True)[:3]

    def gerar_recomendacoes_complementares(self, diagnostico_ia, texto_original):
        """
        Gerar recomendações complementares baseadas na análise
        """
        recomendacoes = []

        # Lógica de recomendações baseada nas categorias de diagnóstico
        for resultado in diagnostico_ia:
            if resultado['probabilidade'] > 0.5:
                categoria = resultado['categoria']

                if categoria == 'Depressão':
                    recomendacoes.append(
                        "Sugere-se acompanhamento psicoterápico e possível avaliação para tratamento medicamentoso."
                    )
                elif categoria == 'Ansiedade':
                    recomendacoes.append(
                        "Recomenda-se técnicas de mindfulness e terapia cognitivo-comportamental."
                    )
                # Adicionar mais categorias conforme necessário

        return recomendacoes

    def comparar_com_base_sintomas(self, texto):
        """
        Comparar o texto com base de sintomas conhecidos
        """
        vetorizador = TfidfVectorizer()

        # Vetorizar o texto do diagnóstico e a base de sintomas
        texto_vetorizado = vetorizador.fit_transform([texto])
        base_vetorizada = vetorizador.transform(self.base_sintomas['descricao'])

        # Calcular similaridade de cosseno
        similaridades = cosine_similarity(texto_vetorizado, base_vetorizada)[0]

        # Encontrar sintomas mais próximos
        indices_top = similaridades.argsort()[-3:][::-1]

        sintomas_relacionados = [
            {
                'sintoma': self.base_sintomas.iloc[idx]['sintoma'],
                'descricao': self.base_sintomas.iloc[idx]['descricao'],
                'similaridade': similaridades[idx]
            } for idx in indices_top
        ]

        return sintomas_relacionados


# Função para integrar no backend
async def processar_diagnostico_ia(texto_diagnostico: str):
    """
    Função para processar diagnóstico usando IA
    """
    assistente = AssistenteIA()

    # Extrair entidades chave
    entidades_chave = assistente.extrair_entidades_chave(texto_diagnostico)

    # Analisar texto com IA
    diagnostico_ia = assistente.analisar_texto_diagnostico(texto_diagnostico)

    # Gerar recomendações
    recomendacoes = assistente.gerar_recomendacoes_complementares(diagnostico_ia, texto_diagnostico)

    # Comparar com base de sintomas
    sintomas_relacionados = assistente.comparar_com_base_sintomas(texto_diagnostico)

    return {
        'diagnostico_ia': diagnostico_ia,
        'entidades_chave': entidades_chave,
        'recomendacoes': recomendacoes,
        'sintomas_relacionados': sintomas_relacionados
    }


# Iniciar servidor
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)