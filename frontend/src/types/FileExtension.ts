export class File_extension {
    // eslint-disable-next-line @typescript-eslint/no-useless-constructor
    constructor(public extension: string) {}

    /**
     * Convert a file extension object to a faculty instance.
     *
     * @param fileExtension
     */
    static fromJSON(fileExtension: File_extension): File_extension {
        return new File_extension(fileExtension.extension);
    }
}
