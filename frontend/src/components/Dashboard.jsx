import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { Target, Trophy, Clock } from 'lucide-react';

const skillData = [
  { subject: 'Python', A: 80, fullMark: 100 },
  { subject: 'SQL', A: 40, fullMark: 100 },
  { subject: 'Pandas', A: 10, fullMark: 100 },
  { subject: 'Data Viz', A: 30, fullMark: 100 },
  { subject: 'Stats', A: 50, fullMark: 100 },
];

const milestoneData = [
  { name: 'Foundations', progress: 100 },
  { name: 'Core Tools', progress: 40 },
  { name: 'Advanced', progress: 0 },
];

export default function Dashboard() {
  return (
    <div className="space-y-6">
      
      {/* Next Recommended Action */}
      <div className="bg-accent/10 border border-accent/20 rounded-2xl p-6 flex flex-col md:flex-row items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-accent mb-1 flex items-center">
            <Target className="w-5 h-5 mr-2" /> Continue Learning
          </h2>
          <p className="text-foreground">You are currently on <strong>Python Fundamentals</strong>. Complete this to unlock Pandas.</p>
        </div>
        <button className="px-6 py-3 bg-accent text-white rounded-xl font-semibold hover:bg-accent/90 transition-colors shrink-0">
          Resume Course
        </button>
      </div>

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
            <p className="text-xs text-muted-foreground">Screen reader alternative: Python (80%), SQL (40%), Pandas (10%), Data Viz (30%), Stats (50%).</p>
          </div>
        </div>

        {/* Milestone Progress Bar Chart */}
        <div className="bg-card border border-border rounded-2xl p-6 shadow-sm">
          <div className="flex items-center mb-4">
            <Clock className="w-5 h-5 text-primary mr-2" />
            <h3 className="font-semibold text-lg">Milestone Progress</h3>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={milestoneData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#ECEEF9" />
                <XAxis type="number" domain={[0, 100]} hide />
                <YAxis dataKey="name" type="category" tick={{ fill: '#1E1B4B', fontSize: 12, fontWeight: 600 }} width={80} axisLine={false} tickLine={false} />
                <Tooltip cursor={{fill: 'transparent'}} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                <Bar dataKey="progress" fill="#7C3AED" radius={[0, 4, 4, 0]} barSize={24} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}
