import React, { useState, useEffect } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { Target, Trophy, Clock, Loader2, Users } from 'lucide-react';
import { api, describeError } from '../lib/api';
import { useToast } from './Toast';
import CourseCard from './CourseCard';

const DEFAULT_SKILL_DATA = [
  { subject: 'Python', A: 0, fullMark: 100 },
  { subject: 'SQL', A: 0, fullMark: 100 },
  { subject: 'Pandas', A: 0, fullMark: 100 },
  { subject: 'Data Viz', A: 0, fullMark: 100 },
  { subject: 'Stats', A: 0, fullMark: 100 },
];

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [skillData, setSkillData] = useState(DEFAULT_SKILL_DATA);
  const [milestoneData, setMilestoneData] = useState([]);
  const [nextAction, setNextAction] = useState(null);
  const [peerRecs, setPeerRecs] = useState([]);
  const toast = useToast();

  useEffect(() => {
    let learnerId = null;
    try { learnerId = localStorage.getItem('learner_id'); } catch {}

    if (!learnerId) {
      setLoading(false);
      return;
    }

    (async () => {
      try {
        const [data, peerData] = await Promise.all([
          api.get(`/analytics/progress/${learnerId}`),
          api.get(`/recommendations/people-like-you/${learnerId}?limit=3`).catch(() => ({ recommendations: [] })),
        ]);
        setSkillData(data.skill_radar || DEFAULT_SKILL_DATA);
        setMilestoneData(data.milestones || []);
        setNextAction(data.next_action || null);
        setPeerRecs(peerData.recommendations || []);
      } catch (err) {
        const msg = describeError(err);
        setError(msg);
        toast.error(`Could not load analytics: ${msg}`);
      } finally {
        setLoading(false);
      }
    })();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <Loader2 className="animate-spin h-8 w-8 text-primary" />
        <span className="ml-3 text-muted-foreground">Loading your analytics...</span>
      </div>
    );
  }

  if (error && skillData === DEFAULT_SKILL_DATA && milestoneData.length === 0) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-2xl p-6 text-center text-red-700">
        Could not load analytics: {error}
      </div>
    );
  }

  const radarAlt = skillData.map(s => `${s.subject} ${s.A}%`).join(', ');

  return (
    <div className="space-y-6">

      {/* Next Recommended Action */}
      {nextAction ? (
        <div className="bg-accent/10 border border-accent/20 rounded-2xl p-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-accent mb-1 flex items-center">
              <Target className="w-5 h-5 mr-2" /> Continue Learning
            </h2>
            <p className="text-foreground">
              You are currently on <strong>{nextAction.skill}</strong>. Complete this to unlock {nextAction.next || 'the next skill'}.
            </p>
          </div>
          <button
            className="px-6 py-3 bg-accent text-white rounded-xl font-semibold hover:bg-accent/90 transition-colors shrink-0"
            onClick={() => window.location.assign('/roadmap')}
          >
            Resume Course
          </button>
        </div>
      ) : (
        <div className="bg-muted/40 border border-border rounded-2xl p-6 text-center text-muted-foreground">
          Complete the chat onboarding or select a career path to see your progress here.
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* Skill Radar Chart */}
        <div className="bg-card border border-border rounded-2xl p-6 shadow-sm">
          <div className="flex items-center mb-4">
            <Trophy className="w-5 h-5 text-primary mr-2" />
            <h3 className="font-semibold text-lg">Skill Development</h3>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={skillData}>
                <PolarGrid stroke="#DDD6FE" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#475569', fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Radar name="Skills" dataKey="A" stroke="#7C3AED" fill="#7C3AED" fillOpacity={0.4} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 border-t border-border pt-4">
            <p className="text-xs text-muted-foreground">Screen reader alternative: {radarAlt}.</p>
          </div>
        </div>

        {/* Milestone Progress Bar Chart */}
        <div className="bg-card border border-border rounded-2xl p-6 shadow-sm">
          <div className="flex items-center mb-4">
            <Clock className="w-5 h-5 text-primary mr-2" />
            <h3 className="font-semibold text-lg">Milestone Progress</h3>
          </div>
          <div className="h-64 w-full">
            {milestoneData.length === 0 ? (
              <div className="h-full flex items-center justify-center text-muted-foreground text-sm">
                No milestones yet — start a learning path.
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={milestoneData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#ECEEF9" />
                  <XAxis type="number" domain={[0, 100]} hide />
                  <YAxis dataKey="name" type="category" tick={{ fill: '#1E1B4B', fontSize: 12, fontWeight: 600 }} width={80} axisLine={false} tickLine={false} />
                  <Tooltip cursor={{fill: 'transparent'}} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                  <Bar dataKey="progress" fill="#7C3AED" radius={[0, 4, 4, 0]} barSize={24} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

      </div>

      {/* People like you also studied */}
      {peerRecs.length > 0 && (
        <div className="bg-card border border-border rounded-2xl p-6 shadow-sm">
          <div className="flex items-center mb-4">
            <Users className="w-5 h-5 text-primary mr-2" />
            <h3 className="font-semibold text-lg">Learners like you also studied</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {peerRecs.map((c) => (
              <CourseCard key={c.id} course={c} compact />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
