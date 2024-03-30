export class Response {
    constructor(
        public message: string,
    ) {
    }

    /**
     * Convert a response object to a response instance.
     *
     * @param response
     */
    static fromJSON(response: Response): Response {
        return new Response(response.message);
    }
}