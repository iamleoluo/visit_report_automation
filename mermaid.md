'''mermaid
    graph TD
        A[Application Layer] -->|Uses| B[Prompt Layer]
        B -->|Uses| C[Chat Layer]
        
        subgraph "Application (auto_summarize.py)"
            A1[Define Business Logic]
            A2[Configure Prompt Templates]
            A3[Handle Application Flow]
        end
        
        subgraph "Prompt Layer (prompt.py)"
            B1[Manage Prompt Templates]
            B2[Handle Conversation History]
            B3[Configure Model Parameters]
        end
        
        subgraph "Chat Layer (chat.py)"
            C1[Ollama Communication]
            C2[Basic Chat Operations]
        end
        
        A1 --> A2 --> A3
        B1 --> B2 --> B3
        C1 --> C2
'''