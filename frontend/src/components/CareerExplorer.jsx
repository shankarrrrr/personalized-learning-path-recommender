import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Filter, 
  Clock, 
  DollarSign, 
  TrendingUp, 
  MapPin, 
  Star,
  ChevronDown,
  ChevronRight,
  BookOpen,
  Target,
  Users,
  Loader2,
  CheckCircle2
} from 'lucide-react';
import { api, describeError } from '../lib/api';
import { useToast } from './Toast';
import { useNavigate } from 'react-router-dom';
import { CareerGridSkeleton } from './Skeletons';

const CareerExplorer = ({ onCareerSelect, selectedCareer }) => {
  const [careers, setCareers] = useState([]);
  const [filteredCareers, setFilteredCareers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filter states
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDomain, setSelectedDomain] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [maxTime, setMaxTime] = useState('');
  const [minSalary, setMinSalary] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [selectedCareerDetails, setSelectedCareerDetails] = useState(null);
  const [selectingCareer, setSelectingCareer] = useState(false);

  const toast = useToast();
  const navigate = useNavigate();

  // Fetch careers on component mount
  useEffect(() => {
    fetchCareers();
  }, []);

  // Apply filters when careers or filter values change
  useEffect(() => {
    applyFilters();
  }, [careers, searchTerm, selectedDomain, selectedDifficulty, maxTime, minSalary]);

  const fetchCareers = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.get('/careers');
      setCareers(data);
    } catch (err) {
      const msg = describeError(err);
      setError(msg);
      toast.error(`Could not load careers: ${msg}`);
    } finally {
      setLoading(false);
    }
  };
  
  const applyFilters = () => {
    let filtered = careers;
    
    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(career =>
        career.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        career.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        career.domain.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    // Domain filter
    if (selectedDomain) {
      filtered = filtered.filter(career => career.domain === selectedDomain);
    }
    
    // Difficulty filter
    if (selectedDifficulty) {
      filtered = filtered.filter(career => career.difficulty_level === selectedDifficulty);
    }
    
    // Time filter
    if (maxTime) {
      filtered = filtered.filter(career => career.estimated_time_months <= parseInt(maxTime));
    }
    
    // Salary filter
    if (minSalary) {
      filtered = filtered.filter(career => career.avg_salary_max >= parseInt(minSalary));
    }
    
    setFilteredCareers(filtered);
  };
  
  const getDomains = () => {
    return [...new Set(careers.map(career => career.domain))];
  };
  
  const getDifficultyLevels = () => {
    return [...new Set(careers.map(career => career.difficulty_level))];
  };
  
  const formatSalary = (min, max) => {
    if (!min || !max) return 'Salary varies';
    return `$${(min/1000).toFixed(0)}k - $${(max/1000).toFixed(0)}k`;
  };
  
  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'Beginner': return 'bg-green-100 text-green-800 border-green-200';
      case 'Intermediate': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'Advanced': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };
  
  const getRemoteFriendlyColor = (remote) => {
    switch (remote) {
      case 'Yes': return 'bg-blue-100 text-blue-800';
      case 'Partial': return 'bg-orange-100 text-orange-800';
      case 'No': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };
  
  const clearFilters = () => {
    setSearchTerm('');
    setSelectedDomain('');
    setSelectedDifficulty('');
    setMaxTime('');
    setMinSalary('');
  };
  
  const handleCareerSelect = async (career) => {
    if (onCareerSelect) {
      onCareerSelect(career);
    }
    setSelectedCareerDetails(career);
  };

  const confirmCareerSelection = async () => {
    if (!selectedCareerDetails) return;
    let learnerId = null;
    try { learnerId = localStorage.getItem('learner_id'); } catch {}

    setSelectingCareer(true);
    try {
      // Persist selection on the backend (updates profile + generates path).
      if (learnerId) {
        await api.post(`/careers/${encodeURIComponent(selectedCareerDetails.id)}/select`, null, {
          query: { learner_id: learnerId },
        });
      }
      toast.success(`Selected ${selectedCareerDetails.title}! Generating your learning path...`);
      setSelectedCareerDetails(null);
      // Give the backend a moment, then take the user to their roadmap.
      setTimeout(() => navigate('/roadmap'), 800);
    } catch (err) {
      const msg = describeError(err);
      toast.error(`Could not select career: ${msg}`);
    } finally {
      setSelectingCareer(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Explore Tech Career Paths</h1>
          <p className="text-lg text-gray-600">Loading career paths...</p>
        </div>
        <CareerGridSkeleton count={6} />
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <div className="text-red-600 mb-2">{error}</div>
        <button 
          onClick={fetchCareers}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }
  
  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Explore Tech Career Paths</h1>
        <p className="text-lg text-gray-600">
          Discover your perfect tech career with comprehensive information about {careers.length} different paths
        </p>
      </div>
      
      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        {/* Search Bar */}
        <div className="relative mb-4">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
          <input
            type="text"
            placeholder="Search career paths, skills, or domains..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        {/* Filter Toggle */}
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <Filter className="h-4 w-4" />
          <span>Advanced Filters</span>
          {showFilters ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
        </button>
        
        {/* Filter Controls */}
        {showFilters && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4 bg-gray-50 rounded-lg">
            {/* Domain Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Domain</label>
              <select
                value={selectedDomain}
                onChange={(e) => setSelectedDomain(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Domains</option>
                {getDomains().map(domain => (
                  <option key={domain} value={domain}>{domain}</option>
                ))}
              </select>
            </div>
            
            {/* Difficulty Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Difficulty</label>
              <select
                value={selectedDifficulty}
                onChange={(e) => setSelectedDifficulty(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Levels</option>
                {getDifficultyLevels().map(level => (
                  <option key={level} value={level}>{level}</option>
                ))}
              </select>
            </div>
            
            {/* Time Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Max Learning Time</label>
              <select
                value={maxTime}
                onChange={(e) => setMaxTime(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Any Duration</option>
                <option value="3">3 months or less</option>
                <option value="6">6 months or less</option>
                <option value="9">9 months or less</option>
                <option value="12">1 year or less</option>
              </select>
            </div>
            
            {/* Salary Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Min Salary</label>
              <select
                value={minSalary}
                onChange={(e) => setMinSalary(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Any Salary</option>
                <option value="60000">$60k+</option>
                <option value="80000">$80k+</option>
                <option value="100000">$100k+</option>
                <option value="120000">$120k+</option>
              </select>
            </div>
            
            {/* Clear Filters */}
            <div className="lg:col-span-4 flex justify-end">
              <button
                onClick={clearFilters}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 underline"
              >
                Clear All Filters
              </button>
            </div>
          </div>
        )}
      </div>
      
      {/* Results Count */}
      <div className="mb-6">
        <p className="text-gray-600">
          Showing {filteredCareers.length} of {careers.length} career paths
        </p>
      </div>
      
      {/* Career Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCareers.map((career) => (
          <div
            key={career.id}
            className={`bg-white rounded-lg shadow-sm border-2 transition-all hover:shadow-md cursor-pointer ${
              selectedCareer?.id === career.id ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-200 hover:border-gray-300'
            }`}
            onClick={() => handleCareerSelect(career)}
          >
            {/* Card Header */}
            <div className="p-6 pb-4">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-1">{career.title}</h3>
                  <p className="text-sm text-gray-500">{career.domain}</p>
                </div>
                {selectedCareer?.id === career.id && (
                  <div className="flex-shrink-0">
                    <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                      <Star className="w-3 h-3 text-white fill-current" />
                    </div>
                  </div>
                )}
              </div>
              
              <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                {career.description}
              </p>
            </div>
            
            {/* Card Stats */}
            <div className="px-6 pb-4 space-y-3">
              {/* Salary */}
              <div className="flex items-center text-sm">
                <DollarSign className="h-4 w-4 text-gray-400 mr-2" />
                <span className="text-gray-600">
                  {formatSalary(career.avg_salary_min, career.avg_salary_max)}
                </span>
              </div>
              
              {/* Time */}
              <div className="flex items-center text-sm">
                <Clock className="h-4 w-4 text-gray-400 mr-2" />
                <span className="text-gray-600">
                  {career.estimated_time_months} months to learn
                </span>
              </div>
              
              {/* Job Growth */}
              {career.job_growth && (
                <div className="flex items-center text-sm">
                  <TrendingUp className="h-4 w-4 text-gray-400 mr-2" />
                  <span className="text-gray-600">{career.job_growth}</span>
                </div>
              )}
              
              {/* Remote Work */}
              <div className="flex items-center text-sm">
                <MapPin className="h-4 w-4 text-gray-400 mr-2" />
                <span className={`px-2 py-1 rounded text-xs font-medium ${getRemoteFriendlyColor(career.remote_friendly)}`}>
                  Remote: {career.remote_friendly}
                </span>
              </div>
            </div>
            
            {/* Card Footer */}
            <div className="px-6 pb-6">
              <div className="flex items-center justify-between">
                <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getDifficultyColor(career.difficulty_level)}`}>
                  {career.difficulty_level}
                </span>
                
                <div className="flex items-center text-sm text-gray-500">
                  <BookOpen className="h-4 w-4 mr-1" />
                  <span>{career.required_skills?.length || 0} skills</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {/* No Results */}
      {filteredCareers.length === 0 && (
        <div className="text-center py-12">
          <Target className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No career paths found</h3>
          <p className="text-gray-500 mb-4">Try adjusting your filters or search terms</p>
          <button
            onClick={clearFilters}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Clear Filters
          </button>
        </div>
      )}
      
      {/* Selected Career Details Modal/Panel would go here */}
      {selectedCareerDetails && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-96 overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-gray-900">{selectedCareerDetails.title}</h2>
                <button
                  onClick={() => setSelectedCareerDetails(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
              
              <div className="space-y-4">
                <p className="text-gray-600">{selectedCareerDetails.description}</p>
                
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-medium">Domain:</span> {selectedCareerDetails.domain}
                  </div>
                  <div>
                    <span className="font-medium">Difficulty:</span> {selectedCareerDetails.difficulty_level}
                  </div>
                  <div>
                    <span className="font-medium">Learning Time:</span> {selectedCareerDetails.estimated_time_months} months
                  </div>
                  <div>
                    <span className="font-medium">Salary Range:</span> {formatSalary(selectedCareerDetails.avg_salary_min, selectedCareerDetails.avg_salary_max)}
                  </div>
                </div>
                
                {selectedCareerDetails.required_skills && selectedCareerDetails.required_skills.length > 0 && (
                  <div>
                    <h4 className="font-medium mb-2">Required Skills:</h4>
                    <div className="flex flex-wrap gap-2">
                      {selectedCareerDetails.required_skills.map((skill, index) => (
                        <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                <button
                  onClick={confirmCareerSelection}
                  disabled={selectingCareer}
                  className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {selectingCareer ? (
                    <><Loader2 className="w-4 h-4 animate-spin" /> Selecting...</>
                  ) : (
                    <>Select This Career Path</>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CareerExplorer;