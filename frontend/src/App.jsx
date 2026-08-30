import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { MessageCircle, Map, LayoutDashboard, Compass } from 'lucide-react';
import OnboardingChat from './components/OnboardingChat';
import RoadmapView from './components/RoadmapView';
import Dashboard from './components/Dashboard';
import CareerExplorer from './components/CareerExplorer';
import ErrorBoundary from './components/ErrorBoundary';
import { ToastProvider } from './components/Toast';

function App() {
  return (
    <Router>
      <ToastProvider>
        <div className="min-h-screen flex flex-col bg-background">
          <nav className="bg-card border-b border-border p-4 sticky top-0 z-10 shadow-sm">
            <div className="max-w-6xl mx-auto flex justify-between items-center">
              <h1 className="text-xl font-bold text-primary">AI Path Recommender</h1>
              <div className="flex space-x-6">
                <Link to="/" className="flex items-center text-muted-foreground hover:text-primary transition-colors">
                  <MessageCircle className="w-5 h-5 mr-1" />
                  <span className="hidden sm:inline">Chat</span>
                </Link>
                <Link to="/careers" className="flex items-center text-muted-foreground hover:text-primary transition-colors">
                  <Compass className="w-5 h-5 mr-1" />
                  <span className="hidden sm:inline">Careers</span>
                </Link>
                <Link to="/roadmap" className="flex items-center text-muted-foreground hover:text-primary transition-colors">
                  <Map className="w-5 h-5 mr-1" />
                  <span className="hidden sm:inline">Roadmap</span>
                </Link>
                <Link to="/dashboard" className="flex items-center text-muted-foreground hover:text-primary transition-colors">
                  <LayoutDashboard className="w-5 h-5 mr-1" />
                  <span className="hidden sm:inline">Dashboard</span>
                </Link>
              </div>
            </div>
          </nav>

          <main className="flex-1 w-full max-w-6xl mx-auto p-4 md:p-8">
            <ErrorBoundary>
              <Routes>
                <Route path="/" element={<OnboardingChat />} />
                <Route path="/careers" element={<CareerExplorer />} />
                <Route path="/roadmap" element={<RoadmapView />} />
                <Route path="/dashboard" element={<Dashboard />} />
              </Routes>
            </ErrorBoundary>
          </main>
        </div>
      </ToastProvider>
    </Router>
  );
}

export default App;
