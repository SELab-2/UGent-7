import { type DockerImage } from './DockerImage';

export class ExtraCheck {
    constructor(
        public id: string = '',
        public name: string = '',
        public docker_image: DockerImage | null = null,
        public file: File | null = null,
        public time_limit: number = 30,
        public memory_limit: number = 128,
        public show_log: boolean = true,
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
