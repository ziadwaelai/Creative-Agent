# Creative Agent Frontend - Streamlit v2.0

A beautiful, user-friendly web interface with **real-time streaming progress** for the Creative Agent API built with Streamlit.

## 🎨 Features

- ✨ **Modern Arabic-Friendly UI** - Fully RTL support with Arabic content
- 📡 **Real-Time Streaming** - Watch each step of content generation in real-time
- ⏱️ **Step-by-Step Progress** - See live updates for each pipeline step (1-6)
- 🎯 **Easy Content Generation** - Simple form to input product and audience information
- 📊 **Real-time Validation** - Character count and field validation as you type
- 📥 **Download Content** - Export generated content as text files
- 🎨 **Beautiful Styling** - Custom CSS with gradient backgrounds and animations
- 📱 **Responsive Design** - Works on desktop and tablet devices
- 🚀 **No Timeout Issues** - Stream-based approach prevents timeout errors

## 📋 Requirements

- Python 3.9+
- Streamlit 1.28+
- Requests library
- Backend API running (see backend README)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install required packages
pip install -r requirements.txt
```

### 2. Start the Backend (if not already running)

```bash
# In another terminal, from the root directory
python -m uvicorn backend.app:app --reload
```

### 3. Run Streamlit App

```bash
# From the frontend directory
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🎯 Usage Guide

### Tab 1: Create Content

1. **Fill in the form:**
   - **Client Name** (1-200 characters): Company or brand name
   - **Product Description** (10-2000 characters): Detailed product information
   - **Target Audience** (5-500 characters): Description of your audience
   - **Tone of Voice**: Select 1-10 desired tones (شاعري, طبيعي, احترافي, etc.)

2. **Click "Generate Content"** (🚀 توليد المحتوى)

3. **View Results:**
   - Generated content displayed in a beautifully formatted box
   - Character count and word count metrics
   - Option to copy content to clipboard
   - Download as text file

### Tab 2: Examples

Pre-built examples for different product types:
- 🧃 Juice Product (عصير)
- ☕ Coffee Product (قهوة)
- 📱 Tech Product (تقني)
- 💄 Beauty Product (جمال)

Click **"استخدم هذا المثال"** to load example data into the form.

### Tab 3: History

View the last generated content and manage your history.

## ⚙️ Configuration

### API URL

By default, the frontend connects to `http://localhost:8000`. You can change this in the sidebar:

1. Open the **Sidebar** (⚙️ الإعدادات)
2. Update the **🔗 عنوان API** field
3. Click **🏥 فحص صحة API** to verify the connection

### Environment Variables (Optional)

Create a `.env` file in the frontend directory:

```env
API_URL=http://localhost:8000
```

## 🎨 UI Components

### Header Section
- App title and subtitle
- Visual branding

### Sidebar
- API configuration
- API health check
- About section with features

### Main Form
- Client name input
- Product description textarea
- Target audience textarea
- Tone of voice multiselect
- Submit and clear buttons
- Real-time validation indicators

### Results Display
- Beautifully formatted content box
- Copy to clipboard button
- Download option
- Metadata display (client, tones, word count, time)

### Tabs
1. **Create Content** - Main form and generation
2. **Examples** - Pre-built templates
3. **History** - Previous results

## 🔒 Security Features

- No sensitive data stored in frontend
- API URL configurable (not hardcoded)
- Input validation on client-side
- Secure communication with backend (HTTPS ready)
- Error handling and user feedback

## 🐛 Troubleshooting

### Connection Errors

**Problem:** "❌ لا يمكن الاتصال بـ API"

**Solutions:**
1. Ensure backend is running:
   ```bash
   python -m uvicorn backend.app:app --reload
   ```
2. Check API URL in sidebar (default: http://localhost:8000)
3. Verify no firewall is blocking the connection

### Timeout Errors

**Problem:** "❌ انتهاء المهلة الزمنية"

**Solutions:**
1. Check internet connection
2. Verify API key is valid in .env
3. Try again - API takes 3-5 seconds to generate

### Validation Errors

**Problem:** "❌ خطأ في البيانات المدخلة"

**Solutions:**
1. Check character counts in validation boxes
2. Ensure all fields are filled
3. Select at least one tone of voice
4. Minimum 10 characters for product description

## 📱 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Production with Streamlit Cloud

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your repository
4. Deploy!

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY frontend/requirements.txt .
RUN pip install -r requirements.txt

COPY frontend/ .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t creative-agent-frontend .
docker run -p 8501:8501 creative-agent-frontend
```

## 🎨 Customization

### Change Colors

Edit the CSS in the `st.markdown()` section:

```python
# Change primary color from #667eea to your color
--primary-color: #your-color;
--secondary-color: #your-color-2;
```

### Add More Examples

Edit the `examples` list in Tab 2:

```python
examples = [
    {
        "name": "Your Product Name",
        "client": "Client Name",
        "product": "Product Description",
        "audience": "Target Audience",
        "tones": ["tone1", "tone2"]
    },
    # Add more examples...
]
```

### Modify Input Constraints

Change field limits in Tab 1:

```python
client_name = st.text_input(..., max_chars=300)  # Increase max chars
product_description = st.text_area(..., height=200)  # Increase height
```

## 📊 Performance

- Page load: < 1 second
- API call: 3-5 seconds (depends on OpenAI API)
- Content display: < 100ms

## 🤝 Integration

This frontend works seamlessly with the Creative Agent backend API. The backend handles:
- Input validation
- AI content generation
- Multiple processing steps
- Error handling

Frontend handles:
- User interface
- Form validation
- API communication
- Results display
- Download functionality

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Requests Library](https://requests.readthedocs.io/)

## 🎓 Code Structure

```
frontend/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Next Steps

1. **Customize styling** to match your brand
2. **Add more product examples** in Tab 2
3. **Integrate analytics** to track usage
4. **Add user authentication** for production
5. **Create mobile app** with Flutter or React Native

## 📄 License

This project is part of the Creative Agency Challenge.

## 👥 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify backend is running and accessible
3. Check browser console for error messages
4. Review Streamlit documentation

## ✨ Key Highlights

- **Easy to Use** - Intuitive interface for anyone
- **Fast** - Instant feedback and results
- **Secure** - No data storage, all processing on backend
- **Scalable** - Works with any backend configuration
- **Beautiful** - Modern design with Arabic support
- **Responsive** - Works on all screen sizes

---

**Ready to generate amazing creative content?** 🚀

Start with the quick start guide above and begin creating!

**Status**: ✅ Production Ready
**Last Updated**: October 26, 2024
