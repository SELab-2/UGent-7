import { User } from '@/types/users/User.ts';
import { Submission } from '@/types/submission/Submission.ts';
import { type HyperlinkedRelation } from '@/types/ApiResponse.ts';

export interface FeedbackJSON {
    id: string;
    message: string;
    creation_date: string;
    author: HyperlinkedRelation;
    submission: HyperlinkedRelation;
}

export class Feedback {
    constructor(
        public id: string = '',
        public message: string = '',
        public creation_date: Date = new Date(),
        public author: User = new User(),
        public submission: Submission = new Submission(),
    ) {}

    static fromJSON(data: FeedbackJSON): Feedback {
        return new Feedback(data.id, data.message, new Date(data.creation_date));
    }
}
