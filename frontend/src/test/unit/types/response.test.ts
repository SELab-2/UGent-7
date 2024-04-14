import { describe, it, expect } from 'vitest';

import { Response } from '@/types/Response';
import { responseData } from './data';
import { createResponse } from './helper';

describe('response type', () => {
    it('create instance of response with correct properties', () => {
        const response = createResponse(responseData);

        expect(response).toBeInstanceOf(Response);
        expect(response.message).toBe(responseData.message);
    });

    it('create a response instance from JSON data', () => {
        const responseJSON = { ...responseData };
        const response = Response.fromJSON(responseJSON);

        expect(response).toBeInstanceOf(Response);
        expect(response.message).toBe(responseData.message);
    });
});
