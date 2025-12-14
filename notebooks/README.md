# The Closer - AI Sales Agent Experimental Notebook

This directory contains a comprehensive Jupyter notebook for experimenting with The Closer AI Sales Agent components.

## Overview

The `the_closer_experiment.ipynb` notebook provides a complete experimental environment to test and validate all components of The Closer agent before full production implementation.

## Features

### 1. **Prospect Intelligence Enricher**
- Company data enrichment (Clearbit integration + fallback)
- Automated fit score calculation
- Buying signal detection
- Pain point identification

### 2. **Email Personalization Engine**
- AI-powered email generation
- Multiple email types (cold outreach, follow-up, value proposition)
- Email validation with 5 criteria checks
- Personalization level control
- Confidence scoring

### 3. **HubSpot Connector** (Mock Mode)
- CRM contact management
- Company lookup
- Interaction note creation
- Mock data for testing without API keys

### 4. **Memory Systems**
- Buyer Persona Memory: 3 pre-defined personas with pain points and successful angles
- Interaction Memory: Track all prospect interactions with sentiment analysis

### 5. **End-to-End Simulation**
- Complete prospecting workflow
- 5-step process from qualification to execution
- Strategy selection based on signals
- Automated tracking setup

### 6. **Experimentation Playground**
- Test different buyer personas
- Adjust fit score weights
- Compare personalization levels
- Interactive parameter tuning

### 7. **Results Analysis**
- Fit score visualizations
- Email validation metrics
- Personalization token analysis
- Performance statistics

## Getting Started

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Install Jupyter
pip install jupyter
```

### Installation

1. **Install Required Packages**

```bash
# Navigate to the notebooks directory
cd notebooks

# Install dependencies
pip install openai httpx tenacity python-dotenv pydantic structlog matplotlib pandas seaborn wordcloud
```

Or install from requirements:

```bash
pip install -r requirements.txt  # If requirements.txt is created
```

2. **Set Up Environment Variables** (Optional)

If you want to use real APIs instead of mock mode:

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

### Running the Notebook

```bash
# Start Jupyter
jupyter notebook

# Open the_closer_experiment.ipynb in your browser
```

## Usage Modes

### Mock Mode (Default)
Perfect for testing without API keys. All tools use realistic mock data.

```python
USE_MOCK_MODE = True  # Set in Section 0
```

**Benefits:**
- No API costs
- Instant responses
- Reproducible results
- Safe for experimentation

### Live API Mode
Connect to real services for production-like testing.

```python
USE_MOCK_MODE = False  # Set in Section 0
```

**Requirements:**
- OpenAI API key (for AI email generation)
- Clearbit API key (optional, for company enrichment)
- HubSpot API key (optional, for CRM integration)

## Notebook Structure

### Section 0: Setup & Configuration
- Package installation
- Environment variables
- API key configuration
- Mock mode toggle

### Section 1: Prospect Intelligence Enricher
- Implementation and testing
- 3 example companies tested
- Fit score calculation demo
- Enriched data display

### Section 2: Email Personalization Engine
- Email generation for multiple types
- 2 buyer personas tested
- Validation results display
- Confidence score analysis

### Section 3: HubSpot Connector (Mock)
- Mock CRM operations
- Contact search and retrieval
- Company lookup
- Note creation

### Section 4: Memory Systems
- Buyer persona definitions (3 personas)
- Interaction tracking
- Memory query examples
- Statistics generation

### Section 5: End-to-End Simulation
- Complete prospect flow
- 5 tasks executed sequentially
- Decision-making logic
- Output display

### Section 6: Experimentation Playground
- Persona comparison
- Fit score sensitivity
- Personalization level testing
- Interactive experiments

### Section 7: Results Analysis
- Fit score visualization
- Email validation charts
- Token usage analysis
- Summary statistics

## Key Components

### Prospect Intelligence Enricher

```python
enricher = ProspectIntelligenceEnricher(use_mock=True)
enriched_data = await enricher.enrich_company("stripe.com")

print(f"Fit Score: {enriched_data.fit_score}/100")
print(f"Industry: {enriched_data.industry}")
print(f"Pain Points: {enriched_data.pain_points}")
```

### Email Personalization Engine

```python
email_engine = EmailPersonalizationEngine(use_mock=True)

email = await email_engine.generate_email(
    email_type=EmailType.COLD_OUTREACH,
    prospect_data=prospect_info,
    personalization_level=PersonalizationLevel.HIGH
)

print(f"Subject: {email.subject}")
print(f"Valid: {email.validation_result.is_valid}")
print(f"Confidence: {email.validation_result.confidence_score}%")
```

### HubSpot Connector

```python
hubspot = HubSpotConnector(use_mock=True)

contacts = await hubspot.search_contacts(query="stripe")
contact = await hubspot.get_contact("1")
note = await hubspot.create_note(contact_id="1", note_body="Call completed")
```

### Memory Systems

```python
# Interaction tracking
interaction_memory = InteractionMemory()

interaction_memory.add_interaction(
    prospect_email="sarah@example.com",
    prospect_name="Sarah Johnson",
    interaction_type=InteractionType.EMAIL_SENT,
    outcome=InteractionOutcome.POSITIVE,
    sentiment_score=0.8
)

history = interaction_memory.get_prospect_history("sarah@example.com")
stats = interaction_memory.get_stats()
```

## Customization

### Adding New Buyer Personas

Edit `BUYER_PERSONAS_EXTENDED` in Section 4:

```python
BUYER_PERSONAS_EXTENDED["New_Persona"] = {
    "role": "Chief Revenue Officer",
    "industry": "Enterprise SaaS",
    "pain_points": ["Revenue predictability", "Sales & Marketing alignment"],
    "motivations": ["ARR growth", "Board reporting"],
    # ... additional fields
}
```

### Modifying Fit Score Weights

Edit the `_calculate_fit_score` method in `ProspectIntelligenceEnricher`:

```python
# Current weights:
# Industry: 30 points
# Company size: 25 points
# Tech stack: 20 points
# Funding: 15 points
# Hiring signals: 10 points
```

### Adding Email Templates

Add new templates to `EMAIL_TEMPLATES` dictionary:

```python
EMAIL_TEMPLATES["new_template"] = {
    "system_prompt": "Your instructions here...",
    "user_prompt_template": "Template with {variables}..."
}
```

## Email Validation Criteria

Emails are validated against 5 criteria:

1. **Subject Length**: Must be < 60 characters
2. **Word Count**: Body must be ≤ 150 words
3. **Pain Point Reference**: Must mention challenges/problems
4. **Clear CTA**: Must include call-to-action
5. **Personalization**: Minimum tokens based on level (1/3/5 for low/medium/high)

**Scoring:**
- Valid: 4+ criteria passed
- Confidence Score: 0-100% based on criteria passed + bonuses

## Test Data Included

### Companies
- Stripe (FinTech, 8000 employees, $2.2B funding)
- Notion (SaaS, 500 employees, $343M funding)
- Figma (SaaS, 800 employees, $332.9M funding)

### Buyer Personas
- VP of Sales (SaaS)
- CTO (Tech Startup)
- VP of Marketing (B2B)

### Sample Prospects
- Sarah Johnson (VP Sales, Acme SaaS)
- David Chen (CTO, TechFlow)
- Multiple test scenarios

## Troubleshooting

### Issue: Notebook cells don't execute

**Solution:**
```bash
# Restart Jupyter kernel
# Kernel > Restart & Clear Output
```

### Issue: Module not found errors

**Solution:**
```bash
pip install --upgrade openai httpx tenacity pydantic structlog matplotlib pandas seaborn
```

### Issue: OpenAI API errors in mock mode

**Solution:**
Verify `USE_MOCK_MODE = True` is set in Section 0

### Issue: Async function errors

**Solution:**
Make sure to use `await` with async functions:
```python
result = await enricher.enrich_company("domain.com")  # ✅ Correct
result = enricher.enrich_company("domain.com")  # ❌ Wrong
```

## API Keys & Security

### Never commit API keys to version control!

Use environment variables or the notebook's secure input:

```python
from getpass import getpass
OPENAI_API_KEY = getpass("OpenAI API Key: ")
```

### API Key Permissions

- **OpenAI**: Requires API access with GPT-3.5/4 permissions
- **Clearbit**: Requires Enrichment API access
- **HubSpot**: Requires CRM and Engagement permissions

## Performance Notes

### Mock Mode Performance
- Enrichment: ~0.5s per company
- Email generation: ~0.3s per email
- HubSpot operations: ~0.1-0.2s

### Live API Mode Performance
- Enrichment: 1-3s (depending on Clearbit)
- Email generation: 2-5s (OpenAI API)
- HubSpot operations: 0.5-2s

## Next Steps

After experimenting with the notebook:

1. **Validate Results**: Review fit scores and email quality
2. **Tune Parameters**: Adjust weights and thresholds
3. **Production Planning**: Design scalable architecture
4. **API Integration**: Implement real API connections
5. **Testing**: Create comprehensive test suite
6. **Deployment**: Set up production environment

## Contributing

To improve this experimental notebook:

1. Test with real data and document results
2. Add new buyer personas based on patterns
3. Refine email templates
4. Enhance fit score algorithm
5. Add new visualizations

## Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Clearbit API Documentation](https://clearbit.com/docs)
- [HubSpot API Documentation](https://developers.hubspot.com/docs/api/overview)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Jupyter Notebook Documentation](https://jupyter-notebook.readthedocs.io/)

## Support

For questions or issues:

1. Check the Troubleshooting section above
2. Review code comments in the notebook
3. Open an issue in the repository
4. Contact the Tokyo-IA team

## License

This notebook is part of the Tokyo-IA project. See the repository LICENSE file for details.

---

**Last Updated**: 2025-12-14
**Version**: 1.0.0
**Author**: Tokyo-IA Team
