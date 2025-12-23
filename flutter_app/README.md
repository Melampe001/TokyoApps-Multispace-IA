# Tokyo-IA Flutter - Complete Autonomous Agents System

🗼 **Tokyo-IA Flutter** is a comprehensive mobile application featuring **7 specialized autonomous AI agents** that operate independently in isolates, providing powerful AI capabilities for code generation, multimedia creation, knowledge management, sentiment analysis, and more.

## 🎯 Overview

This Flutter application implements a sophisticated multi-agent system where each agent:
- Runs in its own **isolate** for true parallelism
- **Boots automatically** on app startup
- Logs all actions to **Firestore** with "verdad absoluta verificada" mark
- Handles errors robustly with retry logic
- Performs health checks continuously

## 🤖 The 7 Autonomous Agents

### 1. 👨‍💻 Agent_CodeMaster (`agent-codemaster-001`)
**Role**: Code generation, review, refactoring, and improvement suggestions

**Capabilities**:
- `generateCode(prompt)`: Generate Flutter/Dart code from natural language
- `reviewCode(code)`: Comprehensive code review with security and performance analysis
- `refactorCode(code, goals)`: Refactor code to meet specific goals
- `suggestImprovements(code)`: Suggest best practices and improvements

**APIs**: Gemini 2.0 Flash, Claude 3.5

### 2. 🎨 Agent_GenAI (`agent-genai-002`)
**Role**: Text-to-Image/Video/Music/Voice generation at 4K quality

**Capabilities**:
- `generateImage(prompt, resolution, style)`: Generate 4K images
- `generateVideo(prompt, duration)`: Create videos with Sora 2 / Veo 3
- `generateMusic(prompt, duration, genre)`: Compose music
- `generateVoice(text, voice, emotion)`: Text-to-speech with emotion

**APIs**: Gemini 2.5 Flash Image, Stability AI, DALL-E 3, ElevenLabs, Sora 2, Veo 3

### 3. 🧠 Agent_Knowledge (`agent-knowledge-003`)
**Role**: RAG (Retrieval Augmented Generation) + real-time web search

**Capabilities**:
- `search(query)`: Real-time web search
- `queryRAG(question, context)`: Query vector knowledge base
- `indexDocument(document)`: Index documents for RAG
- `summarize(content)`: Summarize long content
- `factCheck(statement)`: Verify facts with sources

**APIs**: Google Search API, SerpAPI, Firebase Vector Search, Pinecone, Gemini Pro

### 4. 😊 Agent_Sentiment (`agent-sentiment-004`)
**Role**: Multimodal sentiment analysis and response adaptation

**Capabilities**:
- `analyzeText(text)`: Analyze text sentiment
- `analyzeVoice(audioData)`: Analyze voice tone and emotion
- `analyzeImage(imageData)`: Detect facial expressions
- `adaptResponse(message, sentiment)`: Adapt responses based on user mood
- `detectEmotion(multimodalData)`: Combined emotion detection

**APIs**: Gemini Multimodal, Speech-to-text, Vision API

### 5. 🔓 Agent_Unrestricted (`agent-unrestricted-005`)
**Role**: PIN-protected unrestricted mode management

**Capabilities**:
- `verifyPIN(pin)`: Secure PIN verification
- `enableUnrestrictedMode()`: Enable unrestricted mode with double confirmation
- `disableUnrestrictedMode()`: Disable unrestricted mode
- `checkRestrictions(query)`: Check if query requires unrestricted mode
- `bypassSafetyFilters(prompt)`: Bypass safety filters (with authorization)

**Security Features**:
- Encrypted PIN storage with `flutter_secure_storage`
- Double confirmation required
- Automatic 30-minute timeout
- All activations logged to Firestore

### 6. ✅ Agent_QA (`agent-qa-006`)
**Role**: Quality assurance, commit messages, and PR reviews

**Capabilities**:
- `generateCommitMessage(diff)`: Generate concise, accurate commit messages
- `reviewPullRequest(prData)`: Comprehensive PR review
- `generateChangelogEntry(changes)`: Create changelog entries
- `suggestTests(code)`: Suggest missing test cases
- `checkCodeQuality(files)`: Verify code quality metrics

**Integration**: GitHub API

### 7. 🚀 Agent_Deploy (`agent-deploy-007`)
**Role**: Automated APK/AAB build and deployment

**Capabilities**:
- `buildAPK(flavor, profile)`: Compile APK
- `buildAAB(flavor, profile)`: Compile AAB
- `signBuild(buildPath, keystore)`: Sign builds with encrypted keystore
- `uploadToFirebase(buildPath)`: Upload to Firebase App Distribution
- `generateReleaseNotes(changes)`: Create release notes

**Security**: Encrypted keystore, automatic backup to Firebase Storage

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│           AgentOrchestrator                     │
│  ┌───────────────────────────────────────────┐  │
│  │  Workflow Engine & Task Coordinator       │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ┌────▼───┐   ┌────▼───┐   ┌────▼───┐
   │Isolate │   │Isolate │   │Isolate │
   │Agent 1 │   │Agent 2 │   │Agent 7 │
   └────┬───┘   └────┬───┘   └────┬───┘
        │            │             │
        └────────────┼─────────────┘
                     ▼
            ┌─────────────────┐
            │ FirebaseService │
            │  - Firestore    │
            │  - Vector DB    │
            │  - Storage      │
            └─────────────────┘
```

### Key Components

- **AgentBase**: Abstract base class for all agents with isolate management
- **AgentOrchestrator**: Coordinates all agents, manages workflows
- **FirebaseService**: Handles all Firebase/Firestore operations
- **ApiService**: Makes external API calls with retry logic
- **Models**: AgentTask, AgentResult, AgentLog

## 📦 Installation

### Prerequisites
- Flutter SDK (>=3.0.0)
- Firebase Project configured
- API Keys for AI services (Gemini, Claude, etc.)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA/flutter_app
```

2. **Install dependencies**
```bash
flutter pub get
```

3. **Configure environment variables**

Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

Edit `.env` with your keys:
```env
GEMINI_API_KEY=your_gemini_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
STABILITY_API_KEY=your_stability_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
SERPAPI_KEY=your_serpapi_key
GITHUB_TOKEN=your_github_token
FIREBASE_PROJECT_ID=your_firebase_project_id
UNRESTRICTED_MODE_PIN=your_secure_pin
KEYSTORE_PASSWORD=your_keystore_password
```

4. **Configure Firebase**

- Create a Firebase project at https://console.firebase.google.com
- Add your Android/iOS app
- Download `google-services.json` (Android) and `GoogleService-Info.plist` (iOS)
- Enable Firestore, Storage, and Authentication

5. **Run the app**
```bash
flutter run
```

## 🧪 Testing

Run all tests:
```bash
flutter test
```

Run specific test file:
```bash
flutter test test/agents/agent_code_master_test.dart
```

Run tests with coverage:
```bash
flutter test --coverage
```

## 🔧 Usage Examples

### Initialize Agents
```dart
import 'package:tokyo_ia_flutter/services/agent_orchestrator.dart';

final orchestrator = AgentOrchestrator();
await orchestrator.initializeAllAgents();
```

### Execute a Task
```dart
import 'package:tokyo_ia_flutter/models/agent_task.dart';

final task = AgentTask(
  agentId: 'agent-codemaster-001',
  action: 'generateCode',
  parameters: {
    'prompt': 'Create a Flutter button widget with custom styling',
  },
);

final result = await orchestrator.executeTask('agent-codemaster-001', task);
print(result.output);
```

### Execute a Workflow
```dart
// Smart chat with sentiment adaptation
final workflow = orchestrator.createSmartChatWorkflow('How do I optimize Flutter performance?');
final results = await orchestrator.executeWorkflow(workflow);
```

### Monitor Agent Health
```dart
final healthStatuses = await orchestrator.checkAllAgentsHealth();

for (var entry in healthStatuses.entries) {
  print('${entry.key}: ${entry.value.healthy ? "Healthy" : "Unhealthy"}');
}
```

## 📊 Firestore Schema

### Collections

#### `/agents/{agent_id}`
```json
{
  "name": "CodeMaster",
  "emoji": "👨‍💻",
  "status": "idle",
  "tasks_completed": 42,
  "tasks_failed": 2,
  "last_active": "2025-12-23T08:00:00Z"
}
```

#### `/agent_logs/{log_id}`
```json
{
  "agent_id": "agent-codemaster-001",
  "timestamp": "2025-12-23T08:00:00Z",
  "level": "info",
  "message": "Task completed successfully",
  "verified": true,
  "mark": "verdad absoluta verificada",
  "task_id": "task-123",
  "metadata": {}
}
```

#### `/agent_tasks/{task_id}`
```json
{
  "agent_id": "agent-codemaster-001",
  "action": "generateCode",
  "parameters": {},
  "status": "completed",
  "created_at": "2025-12-23T08:00:00Z",
  "completed_at": "2025-12-23T08:00:05Z",
  "output": {},
  "execution_time_ms": 5000
}
```

## 🔒 Security

- **Never commit API keys**: Use `.env` file (gitignored)
- **PIN encryption**: `flutter_secure_storage` for PIN storage
- **Keystore protection**: Encrypted keystore for release builds
- **Input validation**: All user inputs are validated
- **Output sanitization**: AI outputs are sanitized before display
- **Audit logging**: All sensitive operations logged to Firestore

## 🚀 Deployment

### Debug Build
```bash
flutter build apk --debug
```

### Release Build
```bash
flutter build apk --release
```

### Android App Bundle
```bash
flutter build appbundle --release
```

## 🎨 UI Screens

1. **Home Screen**: Overview of all agents and quick actions
2. **Agents Dashboard**: Monitor agent health, logs, and statistics
3. **Chat Screen**: Interact with agents in real-time

## 🛠️ Troubleshooting

### Firebase initialization fails
- Check `google-services.json` is in `android/app/`
- Verify Firebase project ID in `.env`
- Ensure Firestore is enabled in Firebase Console

### Agent initialization fails
- Check API keys in `.env`
- Verify internet connection
- Check agent logs for specific errors

### Tests fail
- Run `flutter pub get` to update dependencies
- Check that Firebase is properly configured
- Ensure test environment variables are set

## 📝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

## 📄 License

Apache 2.0 - See [LICENSE](../LICENSE) for details.

## 🙏 Acknowledgments

- Built with Flutter and Dart
- AI models: Gemini, Claude, OpenAI, Stability AI, ElevenLabs
- Firebase for backend services
- CrewAI architecture inspiration

## 📞 Support

- Issues: https://github.com/Melampe001/Tokyo-IA/issues
- Documentation: https://github.com/Melampe001/Tokyo-IA/docs

---

**Tokyo-IA Flutter** - Autonomous AI Agents for Mobile 🗼
