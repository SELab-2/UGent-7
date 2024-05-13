import { type DockerImage } from './DockerImage';

export class ExtraCheck {
    constructor(
        public id: string,
        public name: string,
        public docker_image: DockerImage | null,
        public file: File | null,
        public time_limit: number,
        public memory_limit: number,
        public show_log: boolean,
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
            extraCheck.docker_image,
            extraCheck.file,
            extraCheck.time_limit,
            extraCheck.memory_limit,
            extraCheck.show_log,
        );
    }
}
