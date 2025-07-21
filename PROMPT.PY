class PresentationPromptBuilder:
    def __init__(self):
        self.presentation_templates = {
            'business_presentation': {
                'focus': 'professional_services',
                'tone_modifiers': ['authoritative', 'results-driven', 'expert'],
                'cta_patterns': ['Schedule consultation', 'Get started today', 'Learn more']
            },
            'product_showcase': {
                'focus': 'product_benefits', 
                'tone_modifiers': ['compelling', 'feature-focused', 'benefit-driven'],
                'cta_patterns': ['Shop now', 'Try free', 'See pricing']
            },
            'educational_content': {
                'focus': 'knowledge_sharing',
                'tone_modifiers': ['informative', 'accessible', 'engaging'],
                'cta_patterns': ['Download guide', 'Register now', 'Start learning']
            }
        }
    
    def analyze_presentation_type(self, extracted_text: List[str]) -> str:
        """Determine presentation type from content"""
        combined_text = ' '.join(extracted_text).lower()
        
        business_indicators = ['revenue', 'growth', 'strategy', 'market', 'clients']
        product_indicators = ['features', 'benefits', 'pricing', 'demo', 'trial']
        educational_indicators = ['learn', 'guide', 'tutorial', 'steps', 'process']
        
        if sum(1 for word in business_indicators if word in combined_text) >= 2:
            return 'business_presentation'
        elif sum(1 for word in product_indicators if word in combined_text) >= 2:
            return 'product_showcase'
        elif sum(1 for word in educational_indicators if word in combined_text) >= 2:
            return 'educational_content'
        
        return 'business_presentation'  # Default
    
    def build_contextual_prompt(self, extracted_data: Dict, user_tone: str, platform: str) -> str:
        """Build prompt with presentation context"""
        
        # Analyze presentation type
        all_text = []
        for ppt in extracted_data.get('extracted_content', []):
            all_text.extend(ppt.get('extracted_text', []))
        
        presentation_type = self.analyze_presentation_type(all_text)
        template = self.presentation_templates[presentation_type]
        
        # Extract key information
        slide_count = sum(ppt.get('total_slides', 0) for ppt in extracted_data.get('extracted_content', []))
        main_topics = self.extract_main_topics(all_text)
        
        prompt = f"""Act as an expert copywriter specializing in {platform.replace('_', ' ')} advertising.

PRESENTATION ANALYSIS:
- Type: {presentation_type.replace('_', ' ').title()}
- Slides processed: {slide_count}
- Main topics: {', '.join(main_topics[:5])}
- Content focus: {template['focus']}

EXTRACTED CONTENT CONTEXT:
{' '.join(all_text[:800])}...

REQUIREMENTS:
- Tone: {user_tone} (enhanced with {template['tone_modifiers'][0]} approach)
- Platform: {platform.replace('_', ' ').title()}
- Incorporate presentation themes naturally
- Use suggested CTA patterns: {', '.join(template['cta_patterns'])}

Generate 3 unique ad variations that capture the essence of the presentation content while being optimized for {platform}."""
        
        return prompt
    
    def extract_main_topics(self, text_list: List[str]) -> List[str]:
        """Extract main topics from presentation text"""
        # Simple keyword extraction (can be enhanced with NLP)
        from collections import Counter
        import re
        
        # Combine and clean text
        combined = ' '.join(text_list).lower()
        words = re.findall(r'\b[a-z]{4,}\b', combined)
        
        # Filter common words
        stop_words = {'that', 'with', 'have', 'this', 'will', 'your', 'from', 'they', 'been', 'were', 'said', 'each', 'which', 'their', 'time', 'into'}
        meaningful_words = [w for w in words if w not in stop_words]
        
        # Get most common words
        counter = Counter(meaningful_words)
        return [word for word, count in counter.most_common(10)]
