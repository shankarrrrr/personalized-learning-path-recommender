import React from 'react';

/**
 * Skeleton placeholder loaders for loading states. Mirrors the shape of real
 * content so layout doesn't jump when data arrives.
 */

export function CareerCardSkeleton() {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
      <div className="h-6 bg-gray-200 rounded w-3/4 mb-2"></div>
      <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
      <div className="h-3 bg-gray-200 rounded w-full mb-2"></div>
      <div className="h-3 bg-gray-200 rounded w-5/6 mb-4"></div>
      <div className="space-y-2">
        <div className="h-3 bg-gray-200 rounded w-1/3"></div>
        <div className="h-3 bg-gray-200 rounded w-2/5"></div>
        <div className="h-3 bg-gray-200 rounded w-1/4"></div>
      </div>
      <div className="flex justify-between mt-4">
        <div className="h-5 bg-gray-200 rounded-full w-20"></div>
        <div className="h-3 bg-gray-200 rounded w-16"></div>
      </div>
    </div>
  );
}

export function CareerGridSkeleton({ count = 6 }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {Array.from({ length: count }).map((_, i) => (
        <CareerCardSkeleton key={i} />
      ))}
    </div>
  );
}

export function MessageSkeleton() {
  return (
    <div className="flex justify-start">
      <div className="bg-muted rounded-2xl p-4 rounded-bl-none flex space-x-2 items-center">
        <span className="w-2 h-2 bg-primary/50 rounded-full animate-bounce"></span>
        <span className="w-2 h-2 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
        <span className="w-2 h-2 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></span>
      </div>
    </div>
  );
}

export function RoadmapSkeleton({ count = 4 }) {
  return (
    <div className="relative border-l-2 border-border ml-4 space-y-8 pb-12">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="relative pl-8 animate-pulse">
          <div className="absolute -left-[13px] top-4 w-6 h-6 bg-muted rounded-full"></div>
          <div className="p-5 rounded-xl border-2 border-border bg-muted/30">
            <div className="h-5 bg-muted-foreground/20 rounded w-1/2 mb-2"></div>
            <div className="h-3 bg-muted-foreground/20 rounded w-1/3"></div>
          </div>
        </div>
      ))}
    </div>
  );
}
