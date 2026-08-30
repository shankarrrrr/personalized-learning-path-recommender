import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, Loader2, Star, ArrowRight, Clock, DollarSign } from 'lucide-react';
import { api, ApiError, describeError } from '../lib/api';
import { useToast } from './Toast';

export default function OnboardingChat() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hi! I'm your AI learning assistant. What would you like to learn or achieve?" }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [profileId, setProfileId] = useState(() => {
    try { return localStorage.getItem('learner_id') || null; } catch { return null; }
  });
  const [careerSuggestions, setCareerSuggestions] = useState([]);
  const [showCareerSuggestions, setShowCareerSuggestions] = useState(false);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();
  const toast = useToast();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleCareerSelect = async (career) => {
    const userMsg = { role: 'user', content: `I'm interested in becoming a ${career.title}. This sounds like a great fit for me!` };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput('');
    setShowCareerSuggestions(false);
    setIsLoading(true);

    try {
      const data = await api.post('/onboard', {
        messages: newMessages,
        profile_id: profileId ? Number(profileId) : null,
      });
      setMessages(prev => [...prev, data.message]);
      if (data.profile && data.profile.id) {
        setProfileId(data.profile.id);
        try { localStorage.setItem('learner_id', data.profile.id); } catch {}
      }
      if (data.is_complete) {
        setTimeout(() => navigate('/roadmap'), 1500);
      }
    } catch (err) {
      const msg = describeError(err);
      toast.error(msg);
      setMessages(prev => [...prev, { role: 'assistant', content: `Sorry, I ran into an issue: ${msg}` }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExploreAllCareers = () => {
    navigate('/careers');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { role: 'user', content: input };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      const data = await api.post('/onboard', {
        messages: newMessages,
        profile_id: profileId ? Number(profileId) : null,
      });
      setMessages(prev => [...prev, data.message]);
      if (data.profile && data.profile.id) {
        setProfileId(data.profile.id);
        try { localStorage.setItem('learner_id', data.profile.id); } catch {}
      }

      // Handle career suggestions
      if (data.career_suggestions && data.career_suggestions.length > 0) {
        setCareerSuggestions(data.career_suggestions);
        setShowCareerSuggestions(true);
      } else {
        setCareerSuggestions([]);
        setShowCareerSuggestions(false);
      }

      if (data.is_complete) {
        setTimeout(() => navigate('/roadmap'), 1500);
      }
    } catch (err) {
      const msg = describeError(err);
      toast.error(msg);
      setMessages(prev => [...prev, { role: 'assistant', content: `Sorry, I had trouble: ${msg}` }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[80vh] max-w-2xl mx-auto bg-card rounded-2xl shadow-sm border border-border overflow-hidden">
      <div className="p-4 border-b border-border bg-background/50">
        <h2 className="text-lg font-semibold text-primary">Discover Your Path</h2>
        <p className="text-sm text-muted-foreground">Tell me your goals, and I'll generate a custom roadmap.</p>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl p-4 ${
              msg.role === 'user' 
                ? 'bg-primary text-white rounded-br-none' 
                : 'bg-muted text-foreground rounded-bl-none'
            }`}>
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-muted rounded-2xl p-4 rounded-bl-none flex space-x-2 items-center">
              <span className="w-2 h-2 bg-primary/50 rounded-full animate-bounce"></span>
              <span className="w-2 h-2 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
              <span className="w-2 h-2 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></span>
            </div>
          </div>
        )}

        {/* Career Suggestions */}
        {showCareerSuggestions && careerSuggestions.length > 0 && (
          <div className="flex justify-start">
            <div className="max-w-[90%] bg-blue-50 border border-blue-200 rounded-2xl p-4 rounded-bl-none">
              <div className="mb-3">
                <h4 className="font-semibold text-blue-900 mb-1">🎯 Career Path Suggestions</h4>
                <p className="text-sm text-blue-700">Based on your interests, here are some careers that might be perfect for you:</p>
              </div>
              
              <div className="space-y-3">
                {careerSuggestions.map((suggestion, idx) => (
                  <div 
                    key={idx}
                    className="bg-white border border-blue-200 rounded-lg p-3 cursor-pointer hover:bg-blue-50 transition-colors"
                    onClick={() => handleCareerSelect(suggestion)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h5 className="font-medium text-blue-900">{suggestion.title}</h5>
                      <Star className="h-4 w-4 text-yellow-500 fill-current" />
                    </div>
                    <p className="text-sm text-blue-700 mb-2">{suggestion.reason}</p>
                    <div className="flex items-center justify-between text-xs text-blue-600">
                      <span>Click to select this path</span>
                      <ArrowRight className="h-3 w-3" />
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="mt-4 pt-3 border-t border-blue-200">
                <button
                  onClick={handleExploreAllCareers}
                  className="w-full text-center text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center justify-center space-x-1"
                >
                  <span>Explore all {careerSuggestions.length > 0 ? '11' : ''} career paths</span>
                  <ArrowRight className="h-3 w-3" />
                </button>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 bg-background/50 border-t border-border">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="E.g., I want to become a Data Analyst in 3 months..."
            className="flex-1 px-4 py-3 rounded-xl border border-border focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent bg-white"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-primary hover:bg-primary/90 text-white p-3 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
          </button>
        </form>
        <div className="mt-2 text-center space-x-4">
          <button 
            onClick={() => navigate('/roadmap')}
            className="text-xs text-muted-foreground hover:text-primary transition-colors underline"
          >
            Skip for now, use defaults
          </button>
          <button 
            onClick={handleExploreAllCareers}
            className="text-xs text-blue-600 hover:text-blue-800 transition-colors underline"
          >
            Browse all career paths
          </button>
        </div>
      </div>
    </div>
  );
}
