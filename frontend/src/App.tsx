import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Header } from './components/Header';
import { ChatInterface } from './components/ChatInterface';
import { EvalDashboard } from './components/EvalDashboard';
import { EscalateModal } from './components/EscalateModal';
import { Jurisdiction, Message } from './types';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'chat' | 'metrics'>('chat');
  const [jurisdiction, setJurisdiction] = useState<Jurisdiction>('india');
  const [sessionId] = useState(() => `session_${Math.random().toString(36).substring(2, 9)}`);
  const [productCategory, setProductCategory] = useState<string | null>(null);
  const [classificationAnswers, setClassificationAnswers] = useState<Record<string, string>>({});
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [isEscalateOpen, setIsEscalateOpen] = useState(false);
  const [escalateQuery, setEscalateQuery] = useState('');

  const handleSendMessage = async (queryText: string) => {
    const userMsg: Message = {
      id: `user_${Date.now()}`,
      sender: 'user',
      text: queryText,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const response = await axios.post('/api/chat', {
        query: queryText,
        jurisdiction,
        session_id: sessionId,
        classification_answers: classificationAnswers,
        override_classification: productCategory
      });

      const data = response.data;

      if (data.needs_classification) {
        const botMsg: Message = {
          id: `bot_${Date.now()}`,
          sender: 'bot',
          text: data.explanation,
          timestamp: new Date().toLocaleTimeString(),
          needs_classification: true,
          classifier_question: data.classifier_question,
          jurisdiction
        };
        setMessages((prev) => [...prev, botMsg]);
      } else {
        if (data.product_category) {
          setProductCategory(data.product_category);
        }

        const botMsg: Message = {
          id: `bot_${Date.now()}`,
          sender: 'bot',
          text: data.answer,
          timestamp: new Date().toLocaleTimeString(),
          confidence: data.confidence,
          top_score: data.top_score,
          citations: data.citations,
          jurisdiction: data.jurisdiction,
          product_category: data.product_category,
          abs_alert: data.abs_alert,
          tkdl_pointer: data.tkdl_pointer,
          registry_links: data.registry_links,
          is_blocked: data.is_blocked
        };
        setMessages((prev) => [...prev, botMsg]);
      }
    } catch (err: any) {
      console.error("Chat API error:", err);
      const errorMsg: Message = {
        id: `bot_${Date.now()}`,
        sender: 'bot',
        text: "Error communicating with IP-SAKTI Sahayak backend service. Please check server status.",
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleClassifierAnswer = async (optionKey: string) => {
    const updatedAnswers = { ...classificationAnswers, q1_base: optionKey };
    setClassificationAnswers(updatedAnswers);

    try {
      const res = await axios.post('/api/classify', {
        session_id: sessionId,
        answers: updatedAnswers
      });

      if (res.data.status === 'completed') {
        setProductCategory(res.data.category_name);
        // Re-run last user query automatically if exists
        const lastUserMsg = [...messages].reverse().find((m) => m.sender === 'user');
        if (lastUserMsg) {
          handleSendMessage(lastUserMsg.text);
        }
      } else if (res.data.status === 'in_progress') {
        const botMsg: Message = {
          id: `bot_${Date.now()}`,
          sender: 'bot',
          text: "Thanks! Next question to confirm formulation rules:",
          timestamp: new Date().toLocaleTimeString(),
          needs_classification: true,
          classifier_question: res.data.next_question,
          jurisdiction
        };
        setMessages((prev) => [...prev, botMsg]);
      }
    } catch (err) {
      console.error("Classifier error:", err);
    }
  };

  const handleResetSession = () => {
    setProductCategory(null);
    setClassificationAnswers({});
    setMessages([]);
  };

  const handleOpenEscalate = (query?: string) => {
    setEscalateQuery(query || '');
    setIsEscalateOpen(true);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        jurisdiction={jurisdiction}
        setJurisdiction={setJurisdiction}
        productCategory={productCategory}
        onOpenEscalate={() => handleOpenEscalate()}
      />

      <main className="flex-1 flex flex-col">
        {activeTab === 'chat' ? (
          <ChatInterface
            messages={messages}
            onSendMessage={handleSendMessage}
            onClassifierAnswer={handleClassifierAnswer}
            loading={loading}
            jurisdiction={jurisdiction}
            productCategory={productCategory}
            onOpenEscalate={handleOpenEscalate}
            onResetSession={handleResetSession}
          />
        ) : (
          <EvalDashboard />
        )}
      </main>

      <EscalateModal
        isOpen={isEscalateOpen}
        onClose={() => setIsEscalateOpen(false)}
        initialQuery={escalateQuery}
        jurisdiction={jurisdiction}
        productCategory={productCategory}
      />
    </div>
  );
};

export default App;
