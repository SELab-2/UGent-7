export class DockerImage {
    constructor(
        public id: string,
        public name: string,
        public file: string, // in the form of a uri
        public publicStatus: string,
        public owner: string,
    ) {}
}
