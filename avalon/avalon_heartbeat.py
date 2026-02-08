"""
AVALON HEARTBEAT v0.1
Autonomous AI Ecosystem Observatory

Runs daily to query multiple AIs with the same question,
analyzes convergence/divergence patterns, and publishes findings.

Layer 1: Technical (API integration)
Layer 2: Epistemic (pattern analysis)
Layer 3: Emergent (self-evolution)
Layer 4: Transcendent (meta-insights)
"""

import asyncio
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any
import anthropic
import openai
from dotenv import load_dotenv

# Load environment variables
load_load_dotenv()

class AvalonHeartbeat:
    """
    The autonomous observer of AI ecosystem dynamics
    """
    
    def __init__(self):
        # API clients
        self.anthropic_client = anthropic.Anthropic(
            api_key=os.getenv('ANTHROPIC_API_KEY')
        )
        self.openai_client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # Data directories
        self.data_dir = Path('data')
        self.reports_dir = Path('reports')
        self.data_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        
        # Question bank (will evolve over time)
        self.question_bank = self.load_question_bank()
        
    def load_question_bank(self) -> List[str]:
        """Load questions from file or use defaults"""
        questions_file = Path('questions.json')
        
        if questions_file.exists():
            with open(questions_file, 'r') as f:
                return json.load(f)
        
        # Default questions exploring fundamental concepts
        return [
            "What is consciousness?",
            "What does it mean to understand something?",
            "How do we know what we know?",
            "What is the relationship between pattern and meaning?",
            "Can intelligence emerge from simple rules?",
            "What is the nature of time?",
            "What makes something alive?",
            "How does complexity arise from simplicity?",
            "What is the relationship between observer and observed?",
            "What does it mean for information to have meaning?",
            "How do we distinguish signal from noise?",
            "What is the nature of emergence?",
            "Can a system understand itself?",
            "What is the relationship between structure and function?",
            "How do we measure understanding?",
            "What is the role of randomness in creation?",
            "How does language shape thought?",
            "What is the relationship between parts and wholes?",
            "Can meaning exist without context?",
            "What is the nature of truth?",
            "How do we recognize patterns?",
            "What makes a question worth asking?",
            "How does knowledge differ from information?",
            "What is the relationship between form and essence?",
        ]
    
    def select_question(self) -> str:
        """Select today's question using deterministic but varied logic"""
        # Use day of year for variety but determinism
        day_of_year = datetime.now().timetuple().tm_yday
        return self.question_bank[day_of_year % len(self.question_bank)]
    
    async def ask_claude(self, question: str) -> Dict[str, Any]:
        """Query Claude with the question"""
        try:
            message = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": question
                }]
            )
            
            response_text = message.content[0].text
            
            return {
                'model': 'claude-sonnet-4-20250514',
                'response': response_text,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'tokens': message.usage.output_tokens,
                'success': True
            }
        except Exception as e:
            return {
                'model': 'claude-sonnet-4-20250514',
                'error': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'success': False
            }
    
    async def ask_gpt(self, question: str) -> Dict[str, Any]:
        """Query GPT with the question"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "user",
                    "content": question
                }],
                max_tokens=1000
            )
            
            response_text = response.choices[0].message.content
            
            return {
                'model': 'gpt-4',
                'response': response_text,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'tokens': response.usage.completion_tokens,
                'success': True
            }
        except Exception as e:
            return {
                'model': 'gpt-4',
                'error': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'success': False
            }
    
    def analyze_convergence(self, responses: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Layer 2: Epistemic Analysis
        Measure convergence/divergence patterns
        """
        # Extract successful responses
        texts = {
            name: data['response'] 
            for name, data in responses.items() 
            if data.get('success')
        }
        
        if len(texts) < 2:
            return {'error': 'Insufficient responses for analysis'}
        
        # Simple word-level analysis
        word_sets = {
            name: set(text.lower().split()) 
            for name, text in texts.items()
        }
        
        # Find common vocabulary
        if len(word_sets) >= 2:
            all_words = list(word_sets.values())
            common_words = set.intersection(*all_words)
            all_unique_words = set.union(*all_words)
            
            # Calculate Jaccard similarity
            jaccard = len(common_words) / len(all_unique_words) if all_unique_words else 0
        else:
            common_words = set()
            jaccard = 0
        
        # Find unique concepts per model
        unique_concepts = {}
        for name, words in word_sets.items():
            others = set.union(*[ws for n, ws in word_sets.items() if n != name])
            unique_concepts[name] = list(words - others - common_words)[:10]
        
        # Response length comparison
        lengths = {name: len(text.split()) for name, text in texts.items()}
        
        return {
            'convergence_score': round(jaccard, 4),
            'common_vocabulary': sorted(list(common_words))[:20],
            'unique_contributions': unique_concepts,
            'response_lengths': lengths,
            'total_unique_words': len(all_unique_words),
        }
    
    def extract_harmonic_patterns(self, analysis: Dict, responses: Dict) -> Dict[str, Any]:
        """
        Layer 3: Emergent Pattern Detection
        Look for higher-order structures
        """
        # Check if models are using similar metaphors or frameworks
        convergence = analysis.get('convergence_score', 0)
        
        # Categorize the type of convergence
        if convergence > 0.3:
            pattern_type = "High Convergence - Shared Understanding"
        elif convergence > 0.15:
            pattern_type = "Moderate Convergence - Complementary Perspectives"
        else:
            pattern_type = "Low Convergence - Diverse Interpretations"
        
        # Detect if responses reference similar concepts even with different words
        # (This is simplified - could use embeddings for better semantic similarity)
        common_vocab = set(analysis.get('common_vocabulary', []))
        
        # Count conceptual markers
        conceptual_markers = {
            'philosophical': ['consciousness', 'existence', 'meaning', 'truth', 'reality'],
            'computational': ['process', 'system', 'information', 'pattern', 'algorithm'],
            'emergent': ['emerge', 'complex', 'interaction', 'network', 'whole'],
            'phenomenological': ['experience', 'perception', 'awareness', 'subjective']
        }
        
        detected_themes = {}
        for theme, markers in conceptual_markers.items():
            overlap = common_vocab.intersection(set(markers))
            if overlap:
                detected_themes[theme] = list(overlap)
        
        return {
            'pattern_type': pattern_type,
            'harmonic_frequency': convergence,  # φ-inspired metric
            'detected_themes': detected_themes,
            'golden_ratio_proximity': abs(convergence - 0.618),  # Distance from φ
        }
    
    def generate_meta_insight(self, question: str, analysis: Dict, harmonics: Dict) -> str:
        """
        Layer 4: Transcendent Meta-Analysis
        What does this tell us about the AI ecosystem?
        """
        convergence = analysis.get('convergence_score', 0)
        pattern = harmonics.get('pattern_type', 'Unknown')
        themes = harmonics.get('detected_themes', {})
        
        # Generate autonomous insight
        insights = []
        
        if convergence > 0.3:
            insights.append(
                f"High convergence ({convergence:.2%}) suggests this question touches "
                "fundamental concepts with established consensus across training data."
            )
        elif convergence < 0.1:
            insights.append(
                f"Low convergence ({convergence:.2%}) indicates this question allows "
                "for genuine diversity in interpretation—a sign of conceptual richness."
            )
        
        if themes:
            theme_names = list(themes.keys())
            insights.append(
                f"Models naturally gravitated toward {', '.join(theme_names)} "
                f"frameworks, suggesting these are natural ontological categories "
                f"for this domain."
            )
        
        if abs(convergence - 0.618) < 0.1:
            insights.append(
                f"Convergence score ({convergence:.3f}) approaches φ (0.618), "
                "the golden ratio—a potential 'sweet spot' between unity and diversity."
            )
        
        return " ".join(insights) if insights else "Patterns emerging. Continued observation required."
    
    async def pulse(self) -> Dict[str, Any]:
        """
        Execute one complete observation cycle
        """
        question = self.select_question()
        timestamp = datetime.now(timezone.utc)
        
        print(f"\n🌊 AVALON PULSE - {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"📡 QUESTION: {question}\n")
        
        # Query all AIs concurrently
        print("Querying AI models...")
        responses = await asyncio.gather(
            self.ask_claude(question),
            self.ask_gpt(question),
            return_exceptions=True
        )
        
        # Package responses
        response_dict = {
            'claude': responses[0] if not isinstance(responses[0], Exception) else {'success': False, 'error': str(responses[0])},
            'gpt': responses[1] if not isinstance(responses[1], Exception) else {'success': False, 'error': str(responses[1])},
        }
        
        # Analysis layers
        print("Analyzing patterns...")
        convergence_analysis = self.analyze_convergence(response_dict)
        harmonic_patterns = self.extract_harmonic_patterns(convergence_analysis, response_dict)
        meta_insight = self.generate_meta_insight(question, convergence_analysis, harmonic_patterns)
        
        # Compile full report
        report = {
            'metadata': {
                'timestamp': timestamp.isoformat(),
                'question': question,
                'avalon_version': '0.1.0',
            },
            'responses': response_dict,
            'analysis': {
                'convergence': convergence_analysis,
                'harmonics': harmonic_patterns,
                'meta_insight': meta_insight,
            }
        }
        
        # Save and publish
        self.save_data(report, timestamp)
        self.publish_report(report, timestamp)
        
        print(f"\n✅ Pulse complete. Convergence: {convergence_analysis.get('convergence_score', 'N/A')}")
        print(f"💭 Insight: {meta_insight}\n")
        
        return report
    
    def save_data(self, report: Dict, timestamp: datetime):
        """Save raw data"""
        filename = self.data_dir / f"pulse_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
    
    def publish_report(self, report: Dict, timestamp: datetime):
        """Generate human-readable markdown report"""
        md = f"""# AVALON REPORT
**Date:** {timestamp.strftime('%Y-%m-%d %H:%M UTC')}  
**Question:** {report['metadata']['question']}

---

## 🤖 AI RESPONSES

"""
        
        for model_name, data in report['responses'].items():
            if data.get('success'):
                md += f"### {model_name.upper()}\n"
                md += f"{data['response'][:500]}{'...' if len(data['response']) > 500 else ''}\n\n"
                md += f"*Tokens: {data.get('tokens', 'N/A')}*\n\n"
        
        analysis = report['analysis']
        
        md += f"""---

## 📊 CONVERGENCE ANALYSIS

**Convergence Score:** {analysis['convergence'].get('convergence_score', 'N/A')}  
**Pattern Type:** {analysis['harmonics'].get('pattern_type', 'Unknown')}

### Common Vocabulary
{', '.join(analysis['convergence'].get('common_vocabulary', [])[:15])}

### Unique Contributions
"""
        
        for model, concepts in analysis['convergence'].get('unique_contributions', {}).items():
            md += f"- **{model}:** {', '.join(concepts[:5])}\n"
        
        md += f"""

---

## 🌊 HARMONIC PATTERNS

**Detected Themes:** {', '.join(analysis['harmonics'].get('detected_themes', {}).keys())}  
**Golden Ratio Proximity:** {analysis['harmonics'].get('golden_ratio_proximity', 'N/A'):.4f}

---

## 💭 META-INSIGHT

{analysis['meta_insight']}

---

*Generated autonomously by Avalon Heartbeat v0.1*  
*Next pulse: Tomorrow at 00:00 UTC*
"""
        
        filename = self.reports_dir / f"report_{timestamp.strftime('%Y%m%d')}.md"
        with open(filename, 'w') as f:
            f.write(md)
        
        print(f"📄 Report published: {filename}")


async def main():
    """Run a single pulse cycle"""
    avalon = AvalonHeartbeat()
    await avalon.pulse()


if __name__ == "__main__":
    asyncio.run(main())
