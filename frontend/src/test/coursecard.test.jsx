import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import CourseCard from '../components/CourseCard';

const sampleCourse = {
  id: 'python_basics',
  title: 'Python for Everybody',
  description: 'Fundamental programming concepts in Python.',
  platform: 'Coursera',
  level: 'Beginner',
  duration: '6 weeks',
  rating: 4.8,
  is_free: false,
  price: 'Subscription',
  course_url: 'https://example.com/python',
  skills_taught: ['python_basics'],
};

describe('CourseCard', () => {
  it('renders course title and metadata', () => {
    render(<CourseCard course={sampleCourse} />);
    expect(screen.getByText('Python for Everybody')).toBeInTheDocument();
    expect(screen.getByText('Coursera')).toBeInTheDocument();
    expect(screen.getByText('Beginner')).toBeInTheDocument();
    expect(screen.getByText('6 weeks')).toBeInTheDocument();
  });

  it('shows free badge when is_free is true', () => {
    render(<CourseCard course={{ ...sampleCourse, is_free: true }} />);
    expect(screen.getByText('Free')).toBeInTheDocument();
  });

  it('shows price when not free', () => {
    render(<CourseCard course={sampleCourse} />);
    expect(screen.getByText('Subscription')).toBeInTheDocument();
  });

  it('shows rating when present', () => {
    render(<CourseCard course={sampleCourse} />);
    expect(screen.getByText('4.8')).toBeInTheDocument();
  });

  it('renders a View link to the course_url', () => {
    render(<CourseCard course={sampleCourse} />);
    const link = screen.getByText('View').closest('a');
    expect(link).toHaveAttribute('href', 'https://example.com/python');
    expect(link).toHaveAttribute('target', '_blank');
    expect(link).toHaveAttribute('rel', 'noopener noreferrer');
  });

  it('does not render a select button without onSelect/actionLabel', () => {
    render(<CourseCard course={sampleCourse} />);
    expect(screen.queryByRole('button', { name: /select/i })).toBeNull();
  });

  it('calls onSelect with the course when the action button is clicked', async () => {
    const user = userEvent.setup();
    const onSelect = vi.fn();
    render(<CourseCard course={sampleCourse} onSelect={onSelect} actionLabel="Select" />);
    await user.click(screen.getByRole('button', { name: 'Select' }));
    expect(onSelect).toHaveBeenCalledWith(sampleCourse);
  });

  it('renders nothing when course is null', () => {
    const { container } = render(<CourseCard course={null} />);
    expect(container).toBeEmptyDOMElement();
  });

  it('does not crash with missing skills_taught', () => {
    render(<CourseCard course={{ ...sampleCourse, skills_taught: undefined }} />);
    expect(screen.getByText('Python for Everybody')).toBeInTheDocument();
  });

  it('hides description in compact mode', () => {
    render(<CourseCard course={sampleCourse} compact />);
    expect(screen.queryByText('Fundamental programming concepts in Python.')).toBeNull();
  });
});
