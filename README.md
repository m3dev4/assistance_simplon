# 🤖 Assistant Règlement Simplon

Un assistant intelligent alimenté par l'IA qui répond à vos questions sur le règlement intérieur de Simplon Sénégal. Au lieu de parcourir manuellement un long document, vous posez simplement votre question et obtenez une réponse instantanée !

---

## 📋 Table des matières

1. [Comment ça marche ?](#-comment-ça-marche)
2. [Qu'est-ce que le RAG ?](#-quest-ce-que-le-rag)
3. [Structure du projet](#-structure-du-projet)
4. [Les fichiers et leur rôle](#-les-fichiers-et-leur-rôle)
5. [Le Backend (Django)](#-le-backend-django)
6. [L'intégration Frontend (Next.js)](#-lintégration-frontend-nextjs)
7. [Installation et démarrage](#-installation-et-démarrage)
8. [Flux d'une question](#-flux-dune-question)

---

## 🎯 Comment ça marche ?

### L'idée simple

Imaginez que vous avez une **énorme bibliothèque** remplie de livres. Vous posez une question, et au lieu de lire tous les livres manuellement, un assistant intelligent :

1. **Cherche** les passages pertinents dans tous les livres
2. **Les comprend** grâce à l'IA
3. **Vous répond** directement et clairement

C'est exactement ce que fait cet assistant !

### Les étapes principales

```
📄 Règlement PDF
    ↓
📚 Découpé en petits morceaux (chunks)
    ↓
🔢 Converti en chiffres (vecteurs)
    ↓
💾 Stocké dans une base de données (Vector Store)
    ↓
❓ Quelqu'un pose une question
    ↓
🔍 Recherche les passages pertinents
    ↓
🧠 L'IA les analyse et répond
    ↓
✅ Vous obtenez votre réponse !
```

---

## 🧠 Qu'est-ce que le RAG ?

### RAG = Retrieval Augmented Generation

C'est un terme technique qui signifie simplement : **"Rechercher puis générer une réponse"**

#### Sans RAG (IA classique)
L'IA répond en fonction de ce qu'elle a appris pendant son entraînement. Elle peut faire des erreurs ou inventer des informations.

```
Question → IA générale → Réponse (peut être inexacte)
```

#### Avec RAG (Notre système)
L'IA d'abord cherche les informations exactes dans le document, puis les utilise pour répondre.

```
Question → 🔍 Recherche dans le PDF → Passages trouvés → 🧠 IA analyse → Réponse exacte
```

### Avantages du RAG

✅ **Précision** : Les réponses viennent directement du document officiel
✅ **Traçabilité** : On sait d'où vient chaque information
✅ **Actualité** : On peut mettre à jour le document sans réentraîner l'IA
✅ **Pas d'hallucinations** : L'IA n'invente pas, elle cite le document

### Comment le RAG fonctionne en détail

1. **Vecteurs (Embeddings)**
   - Chaque morceau de texte est converti en une liste de chiffres
   - Ces chiffres représentent le "sens" du texte
   - Textes similaires = chiffres similaires
   - Pensez-y comme convertir les mots en une "signature numérique"

2. **Vector Store (Base de données vectorielle)**
   - Stocke tous ces "signatures numériques"
   - Permet une recherche très rapide par similarité

3. **Retriever (Chercheur)**
   - Convertit votre question en vecteur
   - Cherche les passages similaires dans le Vector Store
   - Ramène les 2 passages les plus pertinents

4. **LLM (Grand modèle de langage)**
   - Reçoit votre question + les passages trouvés
   - Génère une réponse claire et bien formulée

---

## 📁 Structure du projet

```
assistance-reglement/                    # 📦 Dossier principal du projet
│
├── app.py                              # 🖥️ Interface Streamlit (optionnel)
├── ingestion.py                        # 🔧 Logique principale du RAG
├── chunks.py                           # ✂️ Découpe du texte en parties
├── vector_store.py                     # 💾 Gestion de la base de données
├── manage.py                           # 🎛️ Outil de commande Django
├── requirements.txt                    # 📋 Dépendances Python
├── db.sqlite3                          # 🗄️ Base de données Django
│
├── chatbot/                            # 🤖 Application Django
│   ├── views.py                        # 👁️ Logique des réponses API
│   ├── serializers.py                  # 📝 Format des données envoyées/reçues
│   ├── models.py                       # 🗄️ Modèles de base de données
│   ├── urls.py                         # 🛣️ Chemins des routes API
│   ├── admin.py                        # 👨‍💼 Interface d'administration
│   ├── apps.py                         # ⚙️ Configuration de l'app
│   └── migrations/                     # 📊 Historique des changements DB
│
├── config/                             # ⚙️ Configuration Django
│   ├── settings.py                     # 🔧 Paramètres généraux
│   ├── urls.py                         # 🛣️ Routes principales
│   ├── asgi.py                         # 🔌 Serveur ASGI
│   ├── wsgi.py                         # 🔌 Serveur WSGI
│   └── __init__.py
│
├── frontend/                           # 🎨 Interface utilisateur
│   ├── app/
│   │   ├── layout.tsx                  # 📄 Structure générale
│   │   ├── page.tsx                    # 🏠 Page principale
│   │   ├── providers.tsx               # 🔌 Fournisseurs (contexte, etc.)
│   │   └── globals.css                 # 🎨 Styles globaux
│   ├── hooks/
│   │   └── useChat.ts                  # 🪝 Hook pour gérer le chat
│   ├── services/
│   │   └── api.ts                      # 📡 Communication avec backend
│   ├── types/
│   │   └── chat.ts                     # 📋 Types TypeScript
│   ├── public/                         # 🖼️ Images et fichiers statiques
│   ├── package.json                    # 📦 Dépendances Node.js
│   ├── next.config.ts                  # ⚙️ Config Next.js
│   └── tsconfig.json                   # ⚙️ Config TypeScript
│
├── data/                               # 📂 Dossier des documents
│   └── re-simplon.pdf                  # 📄 Règlement intérieur en PDF
│
└── vectorstore/                        # 💾 Base de données Chroma
    └── chroma.sqlite3                  # 🗄️ Stockage des vecteurs
```

---

## 📄 Les fichiers et leur rôle

### Backend (Python)

#### `ingestion.py` - Le cœur du RAG 🧠
**Que fait-il ?**
- Charge le PDF du règlement
- Découpe le texte en petits morceaux (chunks)
- Convertit chaque morceau en vecteurs (embeddings)
- Les stocke dans la base de données
- Reçoit les questions et les traite

**Comment ?**
```python
# 1. Charge le PDF
document = charger("re-simplon.pdf")

# 2. Découpe en parties
parties = découper_texte(document)

# 3. Convertit en chiffres (vecteurs)
vecteurs = convertir_en_vecteurs(parties)

# 4. Stocke dans la base
sauvegarder_dans_base(vecteurs)

# 5. Répond aux questions
réponse = chercher_et_répondre("Ma question")
```

#### `chunks.py` - Le découpeur de texte ✂️
**Que fait-il ?**
- Analyse le texte du PDF
- Trouve les articles (Article 1, Article 2, etc.)
- Les découpe intelligemment pour que chaque partie soit cohérente
- Ajoute des métadonnées (numéro d'article, page, etc.)

**Pourquoi ?**
- Si on envoie tout le document à l'IA, elle est confuse
- Les petits morceaux sont faciles à chercher et comprendre

#### `vector_store.py` - Le gestionnaire de base de données 💾
**Que fait-il ?**
- Crée et gère la base de données Chroma
- Stocke les vecteurs (chiffres) de chaque morceau de texte
- Permet des recherches rapides par similarité

**Analogie** : Imaginez une bibliothèque où les livres sont organisés par "sens" plutôt que par ordre alphabétique. Quand vous cherchez quelque chose, on trouve les livres les plus pertinents très rapidement.

### Frontend (TypeScript/React)

#### `services/api.ts` - La connexion au backend 📡
**Que fait-il ?**
- Configure la communication avec le serveur Django
- Envoie les questions au backend
- Reçoit les réponses

**Exemple** :
```typescript
// L'utilisateur pose une question dans le chat
// api.ts la envoie au backend
POST /api/chat → {"question": "Quels sont les horaires ?"}
// Backend répond
← {"answer": "Les horaires sont..."}
```

#### `hooks/useChat.ts` - La logique du chat 🪝
**Que fait-il ?**
- Gère l'historique des messages
- Envoie les messages au backend
- Met à jour l'interface avec les réponses

#### `types/chat.ts` - Les types de données 📋
**Que fait-il ?**
- Définit la structure des données du chat
- Assure que les données sont toujours dans le bon format

#### `app/page.tsx` - La page principale 🏠
**Que fait-il ?**
- Affiche l'interface du chat
- Montre les messages de l'utilisateur et de l'assistant
- Affiche les sources (d'où vient la réponse)

### Configuration (Django)

#### `config/settings.py` - Les paramètres du projet 🔧
**Que fait-il ?**
- Configure Django
- Ajoute les applications (chatbot, rest_framework, corsheaders)
- Configure la base de données
- Active CORS (pour que le frontend puisse communiquer)

#### `config/urls.py` - Les routes principales 🛣️
**Que fait-il ?**
- Définit les chemins d'accès à l'API
- Dirige les requêtes vers les bonnes vues

#### `chatbot/urls.py` - Les routes du chatbot 🛣️
**Que fait-il ?**
- Définit les points d'accès spécifiques du chatbot
- Par exemple: `/api/chat/` pour poser une question

### Application Django

#### `chatbot/views.py` - Les actions possibles 👁️
**Que fait-il ?**
```python
class ChatViewSet:
    def create(self, request):
        # 1. Reçoit la question
        question = request.data["question"]
        
        # 2. Appelle ingestion.py pour obtenir une réponse
        response = ask_question(question)
        
        # 3. Renvoie la réponse au frontend
        return Response({"answer": response["answer"]})
```

#### `chatbot/serializers.py` - Le formateur de données 📝
**Que fait-il ?**
- Valide les données reçues du frontend
- S'assure que la question est dans le bon format
- Convertit les données pour les renvoyer

---

## 🎛️ Le Backend (Django)

### Qu'est-ce que Django ?
Django est un **framework web** pour Python. C'est un ensemble d'outils qui facilite la création d'applications web.

**Analogie** : Django est comme une cuisine pré-équipée. Au lieu de construire tous les outils, vous avez déjà des casseroles, des couteaux, etc. Vous n'avez qu'à cuisiner !

### Comment le backend fonctionne

```
1. Utilisateur pose une question (frontend)
         ↓
2. La question arrive au backend via HTTP
         ↓
3. Django reçoit la requête et la dirige vers ChatViewSet
         ↓
4. ChatViewSet appelle ask_question() (ingestion.py)
         ↓
5. ingestion.py cherche dans le Vector Store
         ↓
6. L'IA génère une réponse
         ↓
7. La réponse est renvoyée au frontend
         ↓
8. L'utilisateur la voit dans le chat
```

### Les API (Points d'accès)

**API** = Une interface qui permet au frontend de communiquer avec le backend

#### Point d'accès principal
```
POST /api/chat/
{
  "question": "Quels sont les horaires de travail ?"
}

Réponse:
{
  "answer": "Les horaires de travail sont de 9h à 17h..."
}
```

### Base de données (db.sqlite3)

- Stocke les informations de Django (utilisateurs, sessions, etc.)
- Léger et idéal pour le développement
- Non utilisée pour le RAG (le RAG utilise Chroma)

---

## 🎨 L'intégration Frontend (Next.js)

### Qu'est-ce que Next.js ?
Next.js est un **framework React** pour créer des interfaces web modernes et rapides.

**Analogie** : Si React est les briques, Next.js est le maçon professionnel qui les assemble de manière efficace.

### Architecture du Frontend

```
Utilisateur tape une question
         ↓
Le composant page.tsx capture le texte
         ↓
useChat.ts envoie la question via api.ts
         ↓
api.ts fait un appel HTTP au backend
         ↓
Backend traite et envoie la réponse
         ↓
useChat.ts met à jour l'état local
         ↓
page.tsx re-affiche avec la nouvelle réponse
         ↓
Utilisateur voit la réponse dans le chat
```

### Flux d'une requête côté frontend

#### Étape 1 : L'utilisateur tape une question
```typescript
// page.tsx reçoit le texte saisi
const [question, setQuestion] = useState("");
```

#### Étape 2 : Envoi de la question
```typescript
// useChat.ts envoie au backend
const sendMessage = async (question) => {
  const response = await apiInstance.post("/chat/", {
    question: question
  });
  return response.data.answer;
};
```

#### Étape 3 : Affichage de la réponse
```typescript
// page.tsx affiche la réponse
<div>{response.answer}</div>
```

### Composants principaux

#### `providers.tsx` - Les fournisseurs 🔌
Donne accès à certaines données à toute l'application (comme une alimentation électrique pour la maison).

#### `globals.css` - Les styles globaux 🎨
Coleurs, polices, espacements... pour toute l'application.

#### Types et hooks
- `useChat.ts` : Logique du chat
- `chat.ts` : Définitions des types

---

## 🚀 Installation et démarrage

### Prérequis

Vous devez avoir installé :
- **Python 3.8+** ([python.org](https://python.org))
- **Node.js + npm** ou **pnpm** ([nodejs.org](https://nodejs.org))
- **Git** ([git-scm.com](https://git-scm.com))

### Installation du Backend

```bash
# 1. Ouvrir un terminal dans le dossier du projet
cd assistance-reglement

# 2. Créer un environnement virtuel Python
python -m venv venv

# 3. Activer l'environnement
# Sur Windows :
venv\Scripts\activate
# Sur Mac/Linux :
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Faire migrer la base de données
python manage.py migrate

# 6. Démarrer le serveur Django
python manage.py runserver
# Le serveur est maintenant accessible à http://localhost:8000
```

### Installation du Frontend

```bash
# 1. Aller dans le dossier frontend
cd frontend

# 2. Installer les dépendances Node.js
npm install
# ou si vous utilisez pnpm :
pnpm install

# 3. Créer un fichier .env.local
# Ajouter : NEXT_PUBLIC_API_URL=http://localhost:8000/api

# 4. Démarrer le serveur de développement
npm run dev
# ou :
pnpm dev

# L'interface est maintenant accessible à http://localhost:3000
```

### Vérifier que tout fonctionne

- Ouvrir http://localhost:3000 dans votre navigateur
- Taper une question sur le règlement
- Vérifier que vous recevez une réponse

---

## ❓ Flux d'une question (Explication complète)

Voici exactement ce qui se passe quand quelqu'un pose une question :

```
TIMELINE DE LA QUESTION:
═══════════════════════════════════════════════════════════════════════════════

T=0s | L'utilisateur tape : "Quels sont les jours de congé ?"
     └─→ Le texte s'affiche dans le chat immédiatement

T=0,1s | Le frontend envoie une requête HTTP au backend :
       POST http://localhost:8000/api/chat/
       {
         "question": "Quels sont les jours de congé ?"
       }

T=0,2s | Django reçoit la requête
       └─→ Dirige vers ChatViewSet.create()

T=0,3s | ChatViewSet appelle ask_question("Quels sont les jours de congé ?")
       └─→ Dans ingestion.py

T=0,4s | ingestion.py :
       ├─→ Convertit la question en vecteur
       └─→ Le cherche dans le Vector Store

T=0,5s | Le Vector Store trouve les 2 passages les plus pertinents :
       ├─→ "Article 4 : Les jours fériés sont..."
       └─→ "Article 5 : Les congés annuels..."

T=0,6s | L'IA (ChatOpenAI via OpenRouter) reçoit :
       ├─→ La question originale
       ├─→ Les 2 passages trouvés
       └─→ Ses instructions (être utile, précis, etc.)

T=0,7s | L'IA génère une réponse naturelle :
       "Les jours de congé sont définis par le règlement...
        Selon l'Article 5, les congés annuels sont accordés..."

T=0,8s | La réponse est renvoyée au frontend

T=0,9s | Le frontend reçoit la réponse et l'affiche

T=1,0s | L'utilisateur voit la réponse complète avec les sources
```

### Données qui circulent

```
QUESTION
    ↓
[Frontend] → (HTTP POST) → [Backend]
    ↑                          ↓
    ↓ (HTTP Response) ← [Ingestion]
    ↓                          ↓
[Display] ← [Vector Store]
                ↓
           [LLM/AI]
```

---

## 🔧 Dépannage

### Le frontend ne peut pas communiquer avec le backend

**Problème** : Erreur CORS ou connexion refusée

**Solutions** :
1. Vérifier que le backend fonctionne : http://localhost:8000
2. Vérifier le fichier `.env.local` du frontend
3. Vérifier que `CORS_ALLOWED_ORIGINS` est configuré dans `config/settings.py`

### Les réponses ne sont pas pertinentes

**Possible causes** :
- Le Vector Store n'a pas été alimenté correctement
- Réexécuter le processus d'ingestion

### Erreur d'API OpenRouter

**Problème** : Clé API invalide ou compte dépassé

**Solution** :
- Vérifier la variable d'environnement `OPENROUTER_API_KEY`
- Vérifier que le compte a du crédit

---

## 📚 Pour aller plus loin

### Technologies utilisées

- **Backend** : Django + Django REST Framework
- **Frontend** : Next.js + TypeScript + React
- **RAG** : LangChain
- **Embeddings** : Ollama (nomic-embed-text)
- **LLM** : OpenRouter (inclusionai/ling-3.0-flash)
- **Vector Store** : Chroma
- **Database** : SQLite + Chroma

### Ressources utiles

- [Django Documentation](https://docs.djangoproject.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [LangChain Documentation](https://js.langchain.com/)
- [Chroma Documentation](https://docs.trychroma.com/)

---

## ✅ Résumé

Cette application utilise le **RAG (Retrieval Augmented Generation)** pour créer un assistant IA capable de répondre précisément aux questions sur le règlement intérieur de Simplon Sénégal.

**Les points clés** :
1. 📄 Le PDF du règlement est découpé en petites parties
2. 🔢 Chaque partie est convertie en "signature numérique" (vecteur)
3. 💾 Ces signatures sont stockées dans une base de données rapide
4. ❓ Quand quelqu'un pose une question, on cherche les passages pertinents
5. 🧠 L'IA utilise ces passages pour générer une réponse précise
6. 🎨 Le frontend affiche la réponse de manière claire

C'est simple, efficace, et garantit que les réponses sont exactes !

---

**Dernière mise à jour** : 27/07/2026  
**Maintenu par** : Mouhamed Lo 
