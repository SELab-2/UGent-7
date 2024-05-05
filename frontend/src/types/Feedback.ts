import {User} from "@/types/users/User.ts";
import {Submission} from "@/types/submission/Submission.ts";

export class Feedback {
    constructor(
        public id: string,
        public message: string,
        public author: User,
        public creation_date: Date,
        public submission: Submission
    ) {}
    static fromJSON(data: any): Feedback {
        return new Feedback(
            data.id,
            data.message,
            data.author,
            data.creation_date,
            data.submission
        );
    }
}