export class FileExtension {
    constructor(
        public id: string = '',
        public extension: string = '',
    ) {}

    /**
     * Convert a file extension object to a file extension instance.
     *
     * @param extension
     */
    static fromJSON(extension: FileExtension): FileExtension {
        return new FileExtension(extension.id, extension.extension);
    }
}
