# 🎉 Festival Emoji Analytics Dashboard
## 🌐 Live Dashboard
The Festival Emoji Analytics Dashboard is deployed on Streamlit Cloud and can be accessed here:

👉 https://emoji-usage-in-festival-tweets-ktfhuutylpshs6kqnv5x79.streamlit.app/
A comprehensive, interactive Streamlit web application for analyzing festival-related social media data, focusing on emoji usage, sentiment analysis, and emotional insights. Built with a dark, neon-themed UI for an engaging user experience.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)

## 🌟 Features

### Core Analytics
- **Real-time KPI Metrics**: Total tweets, unique emojis, top emotions, and trending emojis
- **Interactive Filters**: Filter by festival and sentiment for targeted insights
- **Emoji Frequency Ranking**: Horizontal bar chart showing top emojis
- **Sentiment Distribution**: Pie chart with donut visualization

### Advanced Visualizations
- **Emotion Treemap**: Hierarchical view of emotions and associated emojis
- **Time Series Trends**: Line chart showing tweet activity over time
- **Emoji vs Sentiment Analysis**: Grouped bar chart
- **Tweet Length Distribution**: Violin plot by sentiment
- **Emoji Activity Scatter**: Time-based emoji usage patterns

### Premium Analytics
- **Radar Chart**: Tweet length vs sentiment spider plot
- **Stacked Area Chart**: Sentiment evolution over time
- **Sentiment Gauge**: Speedometer-style positive tweet percentage
- **Sankey Diagram**: Flow from festival → sentiment → emoji
- **Co-occurrence Heatmap**: Emoji correlation matrix
- **Animated Bubble Chart**: Emoji popularity over time
- **Calendar Heatmap**: GitHub-style activity calendar

### User Experience
- **Dark Neon Theme**: Custom CSS with purple accents and dark backgrounds
- **Responsive Design**: Wide layout optimized for desktop and tablets
- **Data Upload**: Excel file upload with automatic column detection
- **Live Data Preview**: Expandable raw data table
- **Error Handling**: Graceful handling of missing columns and data issues

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/festival-emoji-analytics.git
   cd festival-emoji-analytics
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501` (or the port shown in terminal)

## 📊 Data Format

The application expects an Excel file (`.xlsx`) with the following columns:

### Required Columns
- **Festival**: Name of the festival (e.g., "Diwali", "Holi")
- **Sentiment**: Sentiment classification ("Positive", "Negative", "Neutral")
- **Emoji**: Emoji used in the tweet (e.g., "🎉", "❤️")
- **Emotion**: Emotional category (e.g., "Joy", "Sadness")
- **Tweet**: Text content of the tweet

### Optional Columns
- **Date**: Timestamp of the tweet (auto-generated if missing)
- **Author_ID**: User identifier (auto-generated if missing)
- **Tweet_ID**: Unique tweet identifier (auto-generated if missing)

### Sample Data Structure
| Festival | Sentiment | Emoji | Emotion | Tweet |
|----------|-----------|-------|---------|-------|
| Diwali | Positive | 🎉 | Joy | Happy Diwali everyone! |
| Holi | Positive | ❤️ | Love | Colors of love! |
| Diwali | Neutral | 🙏 | Gratitude | Wishing peace |

## 🛠️ Dependencies

```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
numpy>=1.24.0
openpyxl>=3.1.0
```

## 📖 Usage

1. **Upload Data**: Use the sidebar to upload your Excel dataset
2. **Apply Filters**: Select festival and sentiment filters
3. **Explore Visualizations**: Navigate through different chart sections
4. **Adjust Settings**: Use the slider to control number of top emojis shown
5. **View Raw Data**: Expand the data table at the bottom for detailed inspection

## 🎨 Customization

### Theme Customization
The app uses custom CSS for the dark neon theme. Modify the `<style>` section in `app.py` to change colors:

```css
.stApp { background-color: #0E1117; color: white; }
[data-testid="stSidebar"] { background-color: #161B22; }
```

### Adding New Visualizations
Extend the dashboard by adding new Plotly charts in the respective sections of `app.py`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Charts powered by [Plotly](https://plotly.com/)
- Data processing with [Pandas](https://pandas.pydata.org/)

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-username/festival-emoji-analytics/issues) page
2. Create a new issue with detailed description
3. Include your Python version, OS, and error messages

## 🔄 Future Enhancements

- [ ] Real-time data streaming integration
- [ ] Machine learning sentiment analysis
- [ ] Multi-language emoji support
- [ ] Export functionality for charts
- [ ] User authentication and data persistence
- [ ] Mobile-responsive design improvements

---

**Made with ❤️ for festival data enthusiasts**
