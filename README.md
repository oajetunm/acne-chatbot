Acne Skincare PDF Chatbot
An AI-powered chatbot built with Streamlit and LangChain that answers skincare-related questions using information extracted from a dermatologist-approved PDF guide. The app displays product recommendations, prices, and images based on user symptoms such as "cystic acne" or "dark spots".



🚀 Features
💬 Ask natural questions like:

“What’s the best product for dark spots?”

“How do I treat cystic acne?”

🔍 Intelligent retrieval from the PDF guide (using LangChain + embeddings)

🖼️ Product images shown automatically

💵 Price displayed if available in the PDF

⚡ Fast and user-friendly Streamlit interface

📁 Project Structure
bash
Copy
Edit
📦 acne-chatbot/
├── pdf_chatbot.py             # Main Streamlit app
├── acne_guide.pdf             # PDF used for recommendations
├── requirements.txt           # Dependencies
├── .streamlit/
│   └── config.toml            # Streamlit theme config (optional)
├── .gitignore                 # Hides secrets and venv
└── /images/                   # Auto-extracted product images


🧠 Technologies Used
Streamlit – UI framework

LangChain – For Retrieval-Augmented Generation (RAG)

OpenAI API – For generating responses

PyMuPDF (fitz) – To extract images from PDF

PyPDF2 – To extract text from PDF



🧪 How to Run Locally

1. Clone this repository
git clone https://github.com/your-username/acne-chatbot.git
cd acne-chatbot

2. Create a virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Add your OpenAI API key to .env
Create a file named .env with:
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx

5. Run the app
streamlit run pdf_chatbot_app.py
🌐 Deploy to Streamlit Cloud
Push your project to GitHub

Visit streamlit.io/cloud

Click "New App"

Set main file to pdf_chatbot_app.py

Add your OpenAI key in the Secrets tab

✨ Future Improvements
Add multiple PDF support (user-selectable)

Include skin type filters (e.g., oily, dry)

Show comparison tables of recommended products

Save chat history or allow exporting responses

📄 License
This project is open-source under the MIT License.










