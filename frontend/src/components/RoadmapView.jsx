import React, { useState } from 'react';
import { Lock, CheckCircle2, CircleDashed, PlayCircle, MessageCircle, X } from 'lucide-react';

const mockNodes = [
  { id: '1', title: 'SQL Basics', status: 'done', description: 'Learn SELECT, WHERE, JOINs.' },
  { id: '2', title: 'Python Fundamentals', status: 'current', description: 'Variables, loops, and functions in Python.' },
  { id: '3', title: 'Data Manipulation with Pandas', status: 'locked', description: 'DataFrames and data cleaning.' },
  { id: '4', title: 'Machine Learning Intro', status: 'locked', description: 'Supervised vs unsupervised learning.' },
];

export default function RoadmapView() {
  const [nodes, setNodes] = useState(mockNodes);
  const [selectedNode, setSelectedNode] = useState(null);
  const [isUpdating, setIsUpdating] = useState(false);

  const getStatusIcon = (status) => {
    switch(status) {
      case 'done': return <CheckCircle2 className="w-6 h-6 text-green-500" />;
      case 'current': return <CircleDashed className="w-6 h-6 text-primary animate-pulse" />;
      case 'locked': return <Lock className="w-6 h-6 text-muted-foreground" />;
      default: return null;
    }
  };

  const getStatusClass = (status) => {
    switch(status) {
      case 'done': return 'border-green-500 bg-green-50';
      case 'current': return 'border-primary shadow-md bg-white ring-2 ring-primary/20';
      case 'locked': return 'border-border bg-muted/30 text-muted-foreground';
      default: return 'border-border bg-white';
    }
  };

  const markComplete = () => {
    if(!selectedNode) return;
    setIsUpdating(true);
    
    // Mock the re-ranking feedback loop
    setTimeout(() => {
      setNodes(prev => prev.map((n, idx) => {
        if(n.id === selectedNode.id) return { ...n, status: 'done' };
        // Unlock next node
        if(idx > 0 && prev[idx-1].id === selectedNode.id) return { ...n, status: 'current' };
        return n;
      }));
      setSelectedNode(null);
      setIsUpdating(false);
    }, 1000);
  };

  return (
    <div className="flex flex-col md:flex-row gap-6 relative">
      <div className="flex-1 max-w-3xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-foreground">Your Learning Roadmap</h2>
          <p className="text-muted-foreground">Milestone 1: Foundations of Data Analytics</p>
        </div>

        <div className="relative border-l-2 border-border ml-4 space-y-8 pb-12">
          {nodes.map((node, idx) => (
            <div key={node.id} className="relative pl-8">
              <div className="absolute -left-[13px] top-4 bg-background">
                {getStatusIcon(node.status)}
              </div>
              
              <div 
                className={`p-5 rounded-xl border-2 transition-all cursor-pointer ${getStatusClass(node.status)} hover:-translate-y-1 hover:shadow-lg`}
                onClick={() => setSelectedNode(node)}
              >
                <h3 className="font-semibold text-lg">{node.title}</h3>
                <p className="text-sm mt-1 opacity-80">{node.description}</p>
                {node.status === 'done' && <p className="text-xs text-green-600 mt-2 font-medium">Completed</p>}
                {node.status === 'current' && <p className="text-xs text-primary mt-2 font-medium flex items-center"><PlayCircle className="w-3 h-3 mr-1"/> Up Next</p>}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Slide-over Panel for Explainability */}
      {selectedNode && (
        <div className="fixed inset-y-0 right-0 w-full md:w-96 bg-card shadow-2xl border-l border-border p-6 transform transition-transform z-20 flex flex-col">
          <button 
            onClick={() => setSelectedNode(null)}
            className="absolute top-4 right-4 p-2 rounded-full hover:bg-muted text-muted-foreground transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
          
          <h3 className="text-xl font-bold mt-4 pr-8">{selectedNode.title}</h3>
          
          <div className="bg-primary/5 border border-primary/20 p-4 rounded-xl mt-6">
            <h4 className="font-semibold text-primary mb-2 flex items-center">
              <MessageCircle className="w-4 h-4 mr-2" /> Why this?
            </h4>
            <p className="text-sm text-foreground/80 leading-relaxed">
              Recommended because you said you want to work with data pipelines, and this closes your foundational gap before the Pandas module.
            </p>
          </div>

          <div className="mt-8 space-y-3">
            {selectedNode.status === 'current' && (
              <>
                <button 
                  onClick={markComplete}
                  disabled={isUpdating}
                  className="w-full py-3 bg-accent text-white rounded-xl font-medium hover:bg-accent/90 transition-colors disabled:opacity-50 flex justify-center items-center"
                >
                  {isUpdating ? 'Updating Roadmap...' : 'Mark Complete'}
                </button>
                <button className="w-full py-3 bg-white border border-border text-foreground rounded-xl font-medium hover:bg-muted transition-colors">
                  Skip for now
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
