import React, { useState, useEffect } from 'react';
import { Lock, CheckCircle2, CircleDashed, PlayCircle, MessageCircle, X } from 'lucide-react';

export default function RoadmapView() {
  const [nodes, setNodes] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [isUpdating, setIsUpdating] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const learnerId = localStorage.getItem('learner_id');
    if (!learnerId) {
      setIsLoading(false);
      return;
    }
    
    fetch('http://127.0.0.1:8000/path/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ learner_id: parseInt(learnerId) })
    })
    .then(res => res.json())
    .then(data => {
      setNodes(data.ordered_nodes || []);
      setIsLoading(false);
    })
    .catch(err => {
      console.error(err);
      setIsLoading(false);
    });
  }, []);

  const getStatusIcon = (status) => {
    switch(status) {
      case 'completed': return <CheckCircle2 className="w-6 h-6 text-green-500" />;
      case 'current': return <CircleDashed className="w-6 h-6 text-primary animate-pulse" />;
      case 'locked': return <Lock className="w-6 h-6 text-muted-foreground" />;
      case 'skipped': return <CheckCircle2 className="w-6 h-6 text-orange-400" />;
      default: return null;
    }
  };

  const getStatusClass = (status) => {
    switch(status) {
      case 'completed': return 'border-green-500 bg-green-50';
      case 'current': return 'border-primary shadow-md bg-white ring-2 ring-primary/20';
      case 'locked': return 'border-border bg-muted/30 text-muted-foreground';
      case 'skipped': return 'border-orange-400 bg-orange-50';
      default: return 'border-border bg-white';
    }
  };

  const updateProgress = (statusUpdate) => {
    if(!selectedNode) return;
    setIsUpdating(true);
    
    const learnerId = localStorage.getItem('learner_id');
    
    fetch('http://127.0.0.1:8000/progress/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        learner_id: parseInt(learnerId),
        course_id: selectedNode.course_id,
        status: statusUpdate
      })
    })
    .then(res => res.json())
    .then(data => {
      setNodes(data.ordered_nodes || []);
      setSelectedNode(null);
      setIsUpdating(false);
    })
    .catch(err => {
      console.error(err);
      setIsUpdating(false);
    });
  };

  if (isLoading) {
    return <div className="text-center p-12 text-muted-foreground animate-pulse">Generating your personalized roadmap...</div>;
  }

  if (nodes.length === 0) {
    return <div className="text-center p-12 text-muted-foreground">No roadmap found. Please complete the chat onboarding first!</div>;
  }

  return (
    <div className="flex flex-col md:flex-row gap-6 relative">
      <div className="flex-1 max-w-3xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-foreground">Your Learning Roadmap</h2>
          <p className="text-muted-foreground">Personalized Path based on your goals</p>
        </div>

        <div className="relative border-l-2 border-border ml-4 space-y-8 pb-12">
          {nodes.map((node, idx) => (
            <div key={node.skill_id + idx} className="relative pl-8">
              <div className="absolute -left-[13px] top-4 bg-background">
                {getStatusIcon(node.status)}
              </div>
              
              <div 
                className={`p-5 rounded-xl border-2 transition-all cursor-pointer ${getStatusClass(node.status)} hover:-translate-y-1 hover:shadow-lg`}
                onClick={() => setSelectedNode(node)}
              >
                <h3 className="font-semibold text-lg">{node.skill_id.replace(/_/g, ' ').toUpperCase()}</h3>
                <p className="text-sm mt-1 opacity-80">Course ID: {node.course_id}</p>
                {node.status === 'completed' && <p className="text-xs text-green-600 mt-2 font-medium">Completed</p>}
                {node.status === 'skipped' && <p className="text-xs text-orange-500 mt-2 font-medium">Skipped</p>}
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
          
          <h3 className="text-xl font-bold mt-4 pr-8">{selectedNode.skill_id.replace(/_/g, ' ').toUpperCase()}</h3>
          <p className="text-sm text-muted-foreground mt-2">Resource: {selectedNode.course_id}</p>
          
          <div className="bg-primary/5 border border-primary/20 p-4 rounded-xl mt-6">
            <h4 className="font-semibold text-primary mb-2 flex items-center">
              <MessageCircle className="w-4 h-4 mr-2" /> Why this?
            </h4>
            <p className="text-sm text-foreground/80 leading-relaxed">
              Recommended to build your {selectedNode.skill_id.replace(/_/g, ' ')} skills based on your career goals!
            </p>
          </div>

          <div className="mt-8 space-y-3">
            {selectedNode.status === 'current' && (
              <>
                <button 
                  onClick={() => updateProgress('completed')}
                  disabled={isUpdating}
                  className="w-full py-3 bg-accent text-white rounded-xl font-medium hover:bg-accent/90 transition-colors disabled:opacity-50 flex justify-center items-center"
                >
                  {isUpdating ? 'Updating...' : 'Mark Complete'}
                </button>
                <button 
                  onClick={() => updateProgress('skipped')}
                  disabled={isUpdating}
                  className="w-full py-3 bg-white border border-border text-foreground rounded-xl font-medium hover:bg-muted transition-colors"
                >
                  Find Alternative (Skip)
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
