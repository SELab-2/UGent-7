import { type Assistant } from '@/types/users/Assistant.ts';
import { type Teacher } from '@/types/users/Teacher.ts';
import { type Student } from '@/types/users/Student.ts';

export type RoleUser = Student | Teacher | Assistant;
