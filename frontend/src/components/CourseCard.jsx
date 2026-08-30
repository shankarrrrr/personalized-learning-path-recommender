import React from 'react';
import { Star, Clock, DollarSign, ExternalLink, BookOpen } from 'lucide-react';

/**
 * Reusable course card with rich metadata (platform, rating, price, duration).
 * Used in the roadmap slide-over and the "people like you" recommendations.
 */
export default function CourseCard({ course, compact = false, onSelect, actionLabel }) {
  if (!course) return null;

  const rating = course.rating ? Number(course.rating).toFixed(1) : null;
  const priceLabel = course.is_free ? 'Free' : course.price || 'Paid';

  return (
    <div
      className={`bg-card border border-border rounded-xl p-4 transition-all hover:shadow-md ${
        onSelect ? 'cursor-pointer hover:-translate-y-0.5' : ''
      }`}
      onClick={onSelect}
    >
      <div className="flex items-start justify-between gap-2">
        <h4 className="font-semibold text-foreground text-sm leading-snug flex-1">{course.title}</h4>
        {rating && (
          <span className="flex items-center gap-1 text-xs text-amber-600 shrink-0">
            <Star className="w-3.5 h-3.5 fill-amber-500 text-amber-500" />
            {rating}
          </span>
        )}
      </div>

      {!compact && course.description && (
        <p className="text-xs text-muted-foreground mt-2 line-clamp-2">{course.description}</p>
      )}

      <div className="flex flex-wrap gap-2 mt-3 text-[11px]">
        {course.platform && (
          <span className="bg-muted px-2 py-0.5 rounded-full">{course.platform}</span>
        )}
        {course.level && (
          <span className="bg-muted px-2 py-0.5 rounded-full">{course.level}</span>
        )}
        {course.duration && (
          <span className="bg-muted px-2 py-0.5 rounded-full inline-flex items-center gap-1">
            <Clock className="w-3 h-3" /> {course.duration}
          </span>
        )}
        <span className={`px-2 py-0.5 rounded-full inline-flex items-center gap-1 ${course.is_free ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>
          <DollarSign className="w-3 h-3" /> {priceLabel}
        </span>
      </div>

      <div className="flex items-center justify-between mt-3">
        {course.skills_taught && course.skills_taught.length > 0 ? (
          <span className="inline-flex items-center gap-1 text-[11px] text-muted-foreground">
            <BookOpen className="w-3 h-3" />
            {course.skills_taught.length} skill{course.skills_taught.length === 1 ? '' : 's'}
          </span>
        ) : (
          <span />
        )}
        <div className="flex items-center gap-2">
          {course.course_url && (
            <a
              href={course.course_url}
              target="_blank"
              rel="noopener noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="inline-flex items-center gap-1 text-xs text-primary hover:underline"
            >
              <ExternalLink className="w-3.5 h-3.5" /> View
            </a>
          )}
          {actionLabel && onSelect && (
            <button
              onClick={(e) => { e.stopPropagation(); onSelect(course); }}
              className="text-xs bg-primary text-white px-3 py-1 rounded-lg hover:bg-primary/90 transition-colors"
            >
              {actionLabel}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
