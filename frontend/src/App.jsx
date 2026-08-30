import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { MessageCircle, Map, LayoutDashboard, Compass, LogOut, User } from 'lucide-react';
import OnboardingChat from './components/OnboardingChat';
import RoadmapView from './components/RoadmapView';
import Dashboard from './components/Dashboard';
import CareerExplorer from './components/CareerExplorer';
import AuthPage from './components/AuthPage';
import ErrorBoundary from './components/ErrorBoundary';
import { ToastProvider } from './components/Toast';
import { AuthProvider, useAuth } from './lib/auth';

function Nav() {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  return (
    <nav className="bg-card border-b border-border p-4 sticky top-0 z-10 shadow-sm">
      <div className="max-w-6xl mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold text-primary">AI Path Recommender</h1>
        <div className="flex items-center space-x-6">
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
          {isAuthenticated ? (
            <div className="flex items-center gap-2 pl-4 border-l border-border">
              <span className="hidden sm:inline text-sm text-muted-foreground flex items-center">
                <User className="w-4 h-4 mr-1" /> {user?.username}
              </span>
              <button
                onClick={() => { logout(); navigate('/'); }}
                className="flex items-center text-muted-foreground hover:text-primary transition-colors"
                title="Log out"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          ) : (
            <Link to="/login" className="flex items-center text-primary hover:text-primary/80 transition-colors font-medium">
              <User className="w-5 h-5 mr-1" />
              <span className="hidden sm:inline">Sign in</span>
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <ToastProvider>
          <div className="min-h-screen flex flex-col bg-background">
            <Nav />
            <main className="flex-1 w-full max-w-6xl mx-auto p-4 md:p-8">
              <ErrorBoundary>
                <Routes>
                  <Route path="/" element={<OnboardingChat />} />
                  <Route path="/careers" element={<CareerExplorer />} />
                  <Route path="/roadmap" element={<RoadmapView />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/login" element={<AuthPage />} />
                </Routes>
              </ErrorBoundary>
            </main>
          </div>
        </ToastProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
