import React, { useState, useEffect } from 'react';
import { Lock, CheckCircle2, CircleDashed, PlayCircle, MessageCircle, X, Loader2, ExternalLink, Clock, DollarSign } from 'lucide-react';
import { api, describeError } from '../lib/api';
import { useToast } from './Toast';
import { RoadmapSkeleton } from './Skeletons';

export default function RoadmapView() {
  const [nodes, setNodes] = useState([]);
  const [courseDetails, setCourseDetails] = useState({}); // course_id -> Course details
  const [selectedNode, setSelectedNode] = useState(null);
  const [isUpdating, setIsUpdating] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState(null);
  const toast = useToast();

  useEffect(() => {
    let learnerId = null;
    try { learnerId = localStorage.getItem('learner_id'); } catch {}
    if (!learnerId) {
      setIsLoading(false);
      return;
    }

    (async () => {
      try {
        const data = await api.post('/path/generate', { learner_id: parseInt(learnerId) });
        setNodes(data.ordered_nodes || []);
        // Hydrate course details for richer display + "Why this" explanations.
        const ids = [...new Set((data.ordered_nodes || []).map(n => n.course_id))];
        const details = {};
        await Promise.all(ids.map(async (id) => {
          if (id.startsWith('course_for_')) return; // placeholder
          try {
            const c = await api.get(`/courses/${encodeURIComponent(id)}`);
            details[id] = c;
          } catch {}
        }));
        setCourseDetails(details);
      } catch (err) {
        const msg = describeError(err);
        setLoadError(msg);
        toast.error(`Could not load your roadmap: ${msg}`);
      } finally {
        setIsLoading(false);
      }
    })();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

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

  const updateProgress = async (statusUpdate) => {
    if(!selectedNode) return;
    setIsUpdating(true);
    let learnerId = null;
    try { learnerId = localStorage.getItem('learner_id'); } catch {}

    try {
      const data = await api.post('/progress/update', {
        learner_id: parseInt(learnerId),
        course_id: selectedNode.course_id,
        status: statusUpdate
      });
      setNodes(data.ordered_nodes || []);
      setSelectedNode(null);
      toast.success(statusUpdate === 'completed' ? 'Marked as complete! Next skill unlocked.' : 'Found an alternative course for you.');
    } catch (err) {
      const msg = describeError(err);
      toast.error(`Could not update progress: ${msg}`);
    } finally {
      setIsUpdating(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex flex-col md:flex-row gap-6 relative">
        <div className="flex-1 max-w-3xl">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-foreground">Your Learning Roadmap</h2>
            <p className="text-muted-foreground">Generating your personalized path...</p>
          </div>
          <RoadmapSkeleton count={5} />
        </div>
      </div>
    );
  }

  if (loadError && nodes.length === 0) {
    return (
      <div className="text-center p-12 text-muted-foreground">
        <p className="mb-4">We couldn't load your roadmap.</p>
        <button
          onClick={() => window.location.reload()}
          className="text-primary underline hover:text-primary/80"
        >
          Try again
        </button>
      </div>
    );
  }

  if (nodes.length === 0) {
    return <div className="text-center p-12 text-muted-foreground">No roadmap found. Please complete the chat onboarding first!</div>;
  }

  const selectedCourse = selectedNode ? courseDetails[selectedNode.course_id] : null;
  const prettySkill = selectedNode ? selectedNode.skill_id.replace(/_/g, ' ') : '';
  const whyText = selectedCourse
    ? `Recommended because it builds your "${prettySkill}" skills, a key prerequisite for your career goal.`
    : `Recommended to build your ${prettySkill} skills based on your career goals!`;

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
        <div className="fixed inset-y-0 right-0 w-full md:w-96 bg-card shadow-2xl border-l border-border p-6 transform transition-transform z-20 flex flex-col overflow-y-auto">
          <button 
            onClick={() => setSelectedNode(null)}
            className="absolute top-4 right-4 p-2 rounded-full hover:bg-muted text-muted-foreground transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
          
          <h3 className="text-xl font-bold mt-4 pr-8">{selectedNode.skill_id.replace(/_/g, ' ').toUpperCase()}</h3>
          {selectedCourse ? (
            <>
              <p className="text-base font-medium text-primary mt-1">{selectedCourse.title}</p>
              <p className="text-sm text-muted-foreground mt-2">{selectedCourse.description}</p>

              <div className="flex flex-wrap gap-2 mt-4 text-xs">
                {selectedCourse.platform && (
                  <span className="bg-muted px-2 py-1 rounded-full">{selectedCourse.platform}</span>
                )}
                <span className="bg-muted px-2 py-1 rounded-full">{selectedCourse.level}</span>
                <span className="bg-muted px-2 py-1 rounded-full inline-flex items-center gap-1">
                  <Clock className="w-3 h-3" /> {selectedCourse.duration}
                </span>
                <span className={`px-2 py-1 rounded-full inline-flex items-center gap-1 ${selectedCourse.is_free ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>
                  <DollarSign className="w-3 h-3" /> {selectedCourse.is_free ? 'Free' : selectedCourse.price}
                </span>
              </div>

              {selectedCourse.course_url && (
                <a
                  href={selectedCourse.course_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-4 inline-flex items-center gap-1 text-sm text-primary hover:underline"
                >
                  <ExternalLink className="w-4 h-4" /> Open course
                </a>
              )}
            </>
          ) : (
            <p className="text-sm text-muted-foreground mt-2">Resource: {selectedNode.course_id}</p>
          )}
          
          <div className="bg-primary/5 border border-primary/20 p-4 rounded-xl mt-6">
            <h4 className="font-semibold text-primary mb-2 flex items-center">
              <MessageCircle className="w-4 h-4 mr-2" /> Why this?
            </h4>
            <p className="text-sm text-foreground/80 leading-relaxed">
              {whyText}
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
                  {isUpdating ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Updating...</> : 'Mark Complete'}
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
