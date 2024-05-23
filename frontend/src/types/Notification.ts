import moment from 'moment/moment';

export interface NotificationJSON {
    id: string;
    title: string;
    content: string;
    created_at: string;
    is_read: boolean;
    is_sent: boolean;
}

export class Notification {
    constructor(
        public id: string = '',
        public title: string = '',
        public content: string = '',
        public created_at: string = '',
        public is_read: boolean = false,
        public is_sent: boolean = false,
    ) {}

    /**
     * Get the formatted created at date.
     *
     * @returns string
     */
    public getFormattedCreatedAt(): string {
        return moment(this.created_at).format('DD MMMM YYYY');
    }

    /**
     * Get the full name of the user.
     *
     * @param json
     */
    static fromJSON(json: NotificationJSON): Notification {
        return new Notification(json.id, json.title, json.content, json.created_at, json.is_read, json.is_sent);
    }
}
