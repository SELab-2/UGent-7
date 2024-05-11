import { type DockerImage } from './DockerImage';

export class ExtraCheck {
    constructor(
        public id: string,
        public name: string,
        public dockerImage: DockerImage | null,
        public bashFile: File | null,
        public timeLimit: number,
        public memoryLimit: number,
        public showLog: boolean,
    ) {}

    /**
     * Convert an extra check object to a extraCheck instance.
     *
     * @param extraCheck
     */
    static fromJSON(extraCheck: ExtraCheck): ExtraCheck {
        return new ExtraCheck(
            extraCheck.id,
            extraCheck.name,
            null,
            null,
            extraCheck.timeLimit,
            extraCheck.memoryLimit,
            extraCheck.showLog,
        );
    }
}
